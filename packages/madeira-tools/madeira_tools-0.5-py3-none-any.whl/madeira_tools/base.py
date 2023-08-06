from abc import ABC, abstractmethod
import logging

import boto3
from madeira_utils import godaddy_dns, loggers
from madeira import acm, aws_lambda, cloudformation, cloudfront, s3, session, sts


class Base(ABC):

    def __init__(self, app_config, debug=False, mode='test', trace_boto3=False):
        self._logger = loggers.get_logger(level=logging.DEBUG if debug else logging.INFO)

        if mode not in ['test', 'production']:
            raise RuntimeError(f'Invalid mode: {mode}')

        self._mode = mode
        self._logger.info('Using mode: %s', self._mode)
        self._app_config = app_config[self._mode]
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

        if trace_boto3:
            # extreme verbosity in boto3 code paths. useful for tracing AWS API calls that time out
            # after many retries without explaining why (happens with HTTP 500 responses)
            boto3.set_stream_logger('')

    def _init_message(self):
        self._logger.info("AWS account ID: %s", self._sts.account_id)
        self._logger.info("AWS credential profile: %s", self._session.profile_name)
        self._logger.info("AWS default region: %s", self._session.region)

    @abstractmethod
    def deploy(self):
        while False:
            yield None

    @abstractmethod
    def remove(self):
        while False:
            yield None
