#!/bin/bash

( cd app/backend/gtmcore/ && ./install.sh )
( cd app/backend/gtmapi/ && ./install.sh )
( cd app/backend/gtmextraction/ && ./install.sh )
( cd app/backend/gtmprocessing/ && ./install.sh )