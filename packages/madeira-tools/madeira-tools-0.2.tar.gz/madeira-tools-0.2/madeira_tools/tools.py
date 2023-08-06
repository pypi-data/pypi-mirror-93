import json
import logging

import boto3
from madeira_utils import godaddy_dns, utils
import madeira_utils
from madeira import acm, aws_lambda, cloudformation, cloudfront, s3, session, sts


class Tools(object):

    def __init__(self, arguments):
        self._logger = madeira_utils.get_logger(
            level=logging.DEBUG if arguments.get("--debug", False) else logging.INFO)

        self._mode = arguments.get("--mode", 'test')
        if self._mode not in ['test', 'production']:
            raise RuntimeError(f'Invalid mode: {self._mode}')

        self._utils = utils.Utils(logger=self._logger)
        self._logger.info('Using mode: %s', self._mode)
        self._app_config = self._utils.load_yaml('config.yaml')[self._mode]
        self._app_name_lower_case = self._app_config['name'].lower()

        # This Acm instance only to be used to create certificates for CloudFront
        self._acm = acm.Acm(logger=self._logger, region='us-east-1')

        self._aws_lambda = aws_lambda.AwsLambda(logger=self._logger)
        self._cloudformation = cloudformation.CloudFormation(logger=self._logger)
        self._cloudfront = cloudfront.CloudFront(logger=self._logger)
        self._s3 = s3.S3(logger=self._logger)
        self._session = session.Session()
        self._sts = sts.Sts()

        self._g_dns = godaddy_dns.GoDaddyDns(logger=self._logger)

        if arguments.get('--trace-boto3', False):
            # extreme verbosity in boto3 code paths. useful for tracing AWS API calls that time out
            # after many retries without explaining why (happens with HTTP 500 responses)
            boto3.set_stream_logger('')

    def deploy(self):
        self._logger.info("AWS account ID: %s", self._sts.account_id)
        self._logger.info("AWS credential profile: %s", self._session.profile_name)
        self._logger.info("AWS default region: %s", self._session.region)

        ############################################################
        # deploy ACM certificate for CloudFront (must be in us-east-1)
        ############################################################
        acm_certificate_arn, dns_meta = self._acm.request_cert_with_dns_validation(self._app_config['hostname'])
        self._g_dns.assure_value(dns_meta['Name'], dns_meta['Value'], dns_meta['Type'])
        self._acm.wait_for_issuance(acm_certificate_arn)

        ############################################################
        # deploy Lambda Layers for the API
        ############################################################
        layers = {
            self._app_name_lower_case:
                {"path": "layers/api"},
            f"{self._app_name_lower_case}_dependencies":
                {"path": f"layers/{self._app_name_lower_case}_dependencies.zip"},
        }
        self._aws_lambda.deploy_layers(layers)
        layer_arns_csv = ','.join([layer_meta['arn'] for name, layer_meta in layers.items()])
        self._logger.debug(layer_arns_csv)

        ############################################################
        # deploy app infrastructure
        ############################################################
        result = self._cloudformation.create_or_update_stack(
            self._app_config['name'],
            self._utils.get_template_body("app"),
            [
                {"ParameterKey": "ApiConfigurationSecretJson",
                 "ParameterValue": json.dumps(self._app_config)},
                {"ParameterKey": "AppName",
                 "ParameterValue": self._app_config['name']},
                {"ParameterKey": "ApiPersistenceBucketName",
                 "ParameterValue": self._app_config['api_persistence_bucket']},
                {"ParameterKey": "ApiRouterFunctionCode",
                 "ParameterValue": self._utils.get_file_content('functions/router.py')},
                {"ParameterKey": "ApiRouterFunctionLayerArns",
                 "ParameterValue": layer_arns_csv},
                {"ParameterKey": "CdnBucketName",
                 "ParameterValue": self._app_config['cloudfront_ui_bucket']},
                {"ParameterKey": "CertificateArn",
                 "ParameterValue": acm_certificate_arn},
                {"ParameterKey": "HostName",
                 "ParameterValue": self._app_config['hostname']},
            ],
            max_status_checks=30
        )

        if result:
            # upload the UI to the CDN bucket + update CDN cache + assure CNAME is in place
            cdn = self._cloudfront.update_cdn_content(
                self._app_config['cloudfront_ui_bucket'], self._utils.get_files_in_path('assets/'),
                f"Distribution for {self._app_config['name']} - {self._app_config['hostname']}")
            self._g_dns.assure_value(self._app_config['hostname'], cdn['DomainName'], 'CNAME')
            
    def remove(self):
        # Remove DNS entry for app hostname -> CDN
        self._g_dns.delete_value(self._app_config['hostname'], 'CNAME')

        # Remove ACM certificate validation DNS entry
        cert = self._acm.get_cert_by_domain(self._app_config['hostname'])
        dns_meta = self._acm.get_cert_dns_validation_meta(cert['CertificateArn'])
        self._g_dns.delete_value(dns_meta['Name'], dns_meta['Type'])

        # Delete S3 bucket contents
        for bucket in [self._app_config['api_persistence_bucket'], self._app_config['cloudfront_ui_bucket']]:
            self._logger.info('Processing bucket: %s', bucket)

            # purge all objects without versions
            object_keys = self._s3.get_all_object_keys(bucket)
            if object_keys:
                self._logger.info('  deleting objects - please wait')
                objects_deleted = self._s3.delete_objects(bucket, object_keys)
                self._logger.info('  objects deleted: %s', objects_deleted)
            else:
                self._logger.info('  no objects (without version IDs) found')

            # purge all objects with versions + governance bypass
            object_keys = self._s3.get_all_object_versions(bucket)
            if object_keys:
                self._logger.info('  deleting object versions - please wait')
                objects_deleted = self._s3.delete_object_versions(bucket, object_keys)
                self._logger.info('  object versions deleted: %s', objects_deleted)
            else:
                self._logger.info('  no object versions found')

        # Delete CloudFormation stacks
        self._cloudformation.delete_stack(
            self._app_config['name'], disable_termination_protection=True, max_status_checks=30)

        # Delete ACM certificates
        self._acm.delete_cert_by_domain_name(self._app_config['hostname'])

        # Delete lambda layers
        for lambda_layer in self._aws_lambda.list_layers():
            if lambda_layer['LayerName'].startswith(self._app_name_lower_case):
                for lambda_layer_version in self._aws_lambda.list_layer_versions(lambda_layer['LayerName']):
                    self._logger.info('Deleting lambda layer: %s version: %s',
                                      lambda_layer['LayerName'], lambda_layer_version['Version'])
                    self._aws_lambda.delete_layer_version(lambda_layer['LayerArn'], lambda_layer_version['Version'])
