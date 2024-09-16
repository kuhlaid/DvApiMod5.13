# About this repository

This repository hosts a Python package for use with the Dataverse Project API. The purpose of this code is to normalize common API requests for data curation since the Dataverse API has more than one API, which can be confusing to understand which API to use, and which endpoints have quirks under certain conditions. For example, the `createDataset` method allows you to use the same metadata as the `updateDatasetMetadata` method because it automatically wraps the metadata in a `datasetVersion` element (the `create dataset` API endpoint requires the metadata be wrapped in a datasetVersion element for some strange reason).
You can install this package via PIP, but is not hosted on the PIP package service (https://pypi.org/), so you will need to install using a Git command. You can experiment with using this package to build your own packages for a Jupyter notebook.

## Using the package
I use this package with a Jupyter notebook (see the `v5.13/_installer_dataverseTest.py` file in this repository for a working example of the install). The implementation can be found in the `v5.13/_worker_dataverseTest.py` file from https://github.com/kuhlaid/dv-api-test/.