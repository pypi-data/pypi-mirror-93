# Madeira Tools

This is a collection of tools that wraps `madeira` aiming to provide a standard set of functionality
for deployment of test and production apps to AWS.

## Command line tools

`madeira-package_layer <package name> <version>`

* Packages 3rd party dependencies for use as AWS lambda function layers
* Must be run from application project root

`madeira-run-dev`

* Opens XFCE4 terminal with 2 tabs - each for API and UI container runtime + logging
* Must be run from application project root