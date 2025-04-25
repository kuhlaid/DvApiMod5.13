# This file simplifies the commands needed to build the virtual environment for this module,
# create a wheel and push the wheel to PyPi.org test site for testing publication.

# Variables
PYTHON = python3
VENV_DIR = .venv

# since we are running the venv from the Makefile, the venv is not activating and thus `VIRTUAL_ENV` is not automatically exported as an environment variable
# here we set the absolute path to the virtual environment
export VIRTUAL_ENV = $(shell pwd)/$(VENV_DIR)

.PHONY: venvSetup runPyServer dockerBuild createWheel venvCreate
# Commands
# `venvSetup` will first remove an existing venv if it exists and rebuild the environment
# `runPyServer` simply runs jupyter lab

venvCreate:
	( \
		rm -rf $(VENV_DIR); \
		$(PYTHON) -m venv $(VENV_DIR); \
		. .venv/bin/activate; \
		pip install --upgrade pip; \
	)

createWheel:
	( \
       . .venv/bin/activate; \
       $(VENV_DIR)/bin/pip install build; \
	   $(VENV_DIR)/bin/python -m build --wheel; \
    )

# https://twine.readthedocs.io/en/stable/
twineToTest: createWheel
	( \
       . .venv/bin/activate; \
       $(VENV_DIR)/bin/pip install twine; \
	   twine upload -r testpypi dist/*; \
    )

# publish the module to PyPI.org
twineToProd:
	( \
       . .venv/bin/activate; \
       pip install twine; \
	   twine upload dist/*; \
    )