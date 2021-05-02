@echo off
ECHO Pylint Style Checking
pylint --fail-under=7.0 -f text .\github_text_mining\
pause