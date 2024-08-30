# About this repository

This repository hosts a Python package for use with the Dataverse Project API. The package is installed via PIP but is not hosted on the PIP package service (https://pypi.org/). You can experiment with using this package as way to build your own packages for a Jupyter notebook.

## Using the package

I use this package with a Jupyter notebook (see [https://github.com/kuhlaid/dv-api-test/releases/tag/v0.0.3](https://github.com/kuhlaid/dv-api-test/blob/v0.0.3/v5.13/_installer_dataverseTest.py) for a working example of the install).  To see how it is implemented see https://github.com/kuhlaid/dv-api-test/blob/v0.0.3/v5.13/_worker_dataverseTest.py.

## Issues

### 2024-08-30

Tried to get Jupyter notebook to use the latest package code by restarting the kernel of the Jupyter Server. The new code was downloaded but the old package code was still being used. I need to add a version number to the package and test that the package is installed in the Jupyter notebook using the latest version number (must restart the Jupyter server to test this).