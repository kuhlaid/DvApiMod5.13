import versioneer
# setup.py shim for use with applications that require it.
__import__("setuptools").setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)