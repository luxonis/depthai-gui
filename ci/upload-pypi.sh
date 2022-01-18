#!/bin/bash

/opt/python/cp38-cp38/bin/python3.8 -m pip install -U pip
/opt/python/cp38-cp38/bin/python3.8 -m pip install -U setuptools
/opt/python/cp38-cp38/bin/python3.8 -m pip install -U twine

# Uploads prebuilt binary distribution
for file in wheelhouse/audited/*.whl; do
    echo "Uploading $file"
    /opt/python/cp38-cp38/bin/python3.8 -m twine upload --repository-url "$PYPI_SERVER" --username "$PYPI_USER" --password "$PYPI_PASSWORD" "$file"
done

# Uploads zip source distribution
for file in wheelhouse/audited/*.zip; do
    echo "Uploading $file"
    /opt/python/cp38-cp38/bin/python3.8 -m twine upload --repository-url "$PYPI_SERVER" --username "$PYPI_USER" --password "$PYPI_PASSWORD" "$file"
done

# Uploads tar.gz source distribution
for file in wheelhouse/audited/*.tar.gz; do
    echo "Uploading $file"
    /opt/python/cp38-cp38/bin/python3.8 -m twine upload --repository-url "$PYPI_SERVER" --username "$PYPI_USER" --password "$PYPI_PASSWORD" "$file"
done