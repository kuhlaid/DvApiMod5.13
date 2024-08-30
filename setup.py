# setup.py shim for use with applications that require it.
# NOTE: we need to change the version when we push an update so that users will not need to restart their Jupyter Server to install the latest package and so users know the version they are installing
# TODO: we could try https://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package for automating the version number generation

# pull in the __version__ constant from the package
from DvApiMod-pip-package import __version__

__import__("setuptools").setup(
    version=__version__
)

# version="1.0.1",  # removed this from the setup to see if the pyproject.toml will take care of it