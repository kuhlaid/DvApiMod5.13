# setup.py shim for use with applications that require it.
# NOTE: we need to change the version when we push an update so that users will not need to restart their Jupyter Server to install the latest package and so users know the version they are installing
# If a 'version' file can be generated automatically from GitHub actions then we could use that

__import__("setuptools").setup(
    version="1.0.2"
)