#!/bin/bash

echo "Pylint Style Checking"
pylint --fail-under=7.0 -f text src/backend/gtmcore/gtmcore src/backend/gtmapi/gtmapi src/backend/gtmextraction/gtmextraction src/backend/gtmprocessing/gtmprocessing