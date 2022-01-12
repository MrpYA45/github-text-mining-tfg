#!/bin/bash

TEMP_DIR="$(mktemp -d)"

# Install
cp -R * "${TEMP_DIR}"
pushd "${TEMP_DIR}"
./setup.py install
cd /
FILES_DIR=$(python3 -c "import gtmprocessing
import os
print(os.path.dirname(gtmprocessing.__file__))")
cp -R "${TEMP_DIR}"/gtmprocessing/data/models "${FILES_DIR}"/data/
popd

rm -R "${TEMP_DIR}"