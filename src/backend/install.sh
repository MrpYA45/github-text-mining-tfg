#!/bin/bash
PATH_GTM="$(pwd)"

( cd app/backend/gtmcore/ && ./install.sh )
( cd app/backend/gtmapi/ && ./install.sh )
( cd app/backend/gtmextraction/ && ./install.sh )