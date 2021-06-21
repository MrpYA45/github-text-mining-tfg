#!/bin/bash

set -xe

cd /app/core
./install.sh

cd /app/src
./install.sh
./run.sh