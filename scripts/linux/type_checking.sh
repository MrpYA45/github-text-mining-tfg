#!/bin/bash

SUCCESS=0

echo "MyPy Type Checking"

echo "[GTMCORE]"
mypy src/backend/gtmcore/gtmcore
SUCCESS=$((${SUCCESS}+$?))

echo "[GTMAPI]"
mypy src/backend/gtmapi/gtmapi src/backend/gtmcore/gtmcore
SUCCESS=$((${SUCCESS}+$?))

echo "[GTMEXTRACTION]"
mypy src/backend/gtmextraction/gtmextraction src/backend/gtmcore/gtmcore
SUCCESS=$((${SUCCESS}+$?))

echo "[GTMPROCESSING]"
mypy src/backend/gtmprocessing/gtmprocessing src/backend/gtmcore/gtmcore
SUCCESS=$((${SUCCESS}+$?))

exit ${SUCCESS}