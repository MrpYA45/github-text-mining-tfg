#!/bin/bash
app/backend/gtmapi/bin/gtmapi & 
(sleep 10 && app/backend/gtmextraction/bin/gtmextraction)