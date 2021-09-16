#!/bin/bash

TEMP_DIR="$(mktemp -d)"

# Install
cp -R * "${TEMP_DIR}"
pushd "${TEMP_DIR}"
./setup.py install
FILES_DIR="%(pwd)"
cp -R gtmprocessing/data/models "${PREV_DIR}"/gtmprocessing/data/
popd

rm -R "${TEMP_DIR}"