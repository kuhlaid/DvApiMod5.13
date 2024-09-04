# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.0.4] - 2024-09-04

- [x] **IMPORTANT** change methods to allow for passing in parameters instead of assuming other users will be using the same JSON configuration
- [x] fixing issue with `printResponseInfo` method not handling missing JSON response correctly

## [v1.0.3] - 2024-09-03

- [x] changing the `addDatasetFile` to allow for passing the file upload parameters to this method so users are not forced to use a set JSON format in their metadata
- [x] need to add a package version so that when users install the package, the package version is shown to the user (consider trying to use https://github.com/python-versioneer/python-versioneer/); tried several ways and hard-coding the version into the `setup.py` script is the sane way for now

## [v1.0.1] - 2024-08-30

- [x] pushing new version to see if that corrects the caching issue in the Jupyter notebook (it did not correct the issue)

## [v1.0] - 2024-08-28

- [x] finished testing moving the code from local to remote install from GitHub