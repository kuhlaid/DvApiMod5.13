# setup.py shim for use with applications that require it.
__import__("setuptools").setup()

from DvApiMod_pip_package import __version__

setup(
    name='DvApiMod_pip_package',
    version=__version__,
    url='https://github.com/kuhlaid/DvApiMod5.13',
    author='w. Patrick Gale',
    author_email='w.patrick.gale@gmail.com'
)
