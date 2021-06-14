#!/bin/bash
app/backend/gtmapi/bin/gtmapi & 
(sleep 10 && app/backend/gtmextraction/bin/gtmextraction) &
(sleep 10 && app/backend/gtmprocessing/bin/gtmprocessing)