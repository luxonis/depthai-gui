#!/bin/bash

/opt/python/cp38-cp38/bin/python3.8 -m pip install -U pip
/opt/python/cp38-cp38/bin/python3.8 -m pip install -U setuptools
/opt/python/cp38-cp38/bin/python3.8 -m pip install -U twine

/opt/python/cp38-cp38/bin/python3.8 -m twine upload --repository-url "$PYPI_SERVER" --username "$PYPI_USER" --password "$PYPI_PASSWORD" wheelhouse/audited/*
