@echo off

SET /A SUCCESS=0

ECHO MyPy Type Checking

ECHO [GTMCORE]
mypy src\backend\gtmcore\gtmcore
SET /A SUCCESS=%SUCCESS%+%errorlevel%

ECHO [GTMAPI]
mypy src\backend\gtmapi\gtmapi src\backend\gtmcore\gtmcore
SET /A SUCCESS=%SUCCESS%+%errorlevel%

ECHO [GTMEXTRACTION]
mypy src\backend\gtmextraction\gtmextraction src\backend\gtmcore\gtmcore
SET /A SUCCESS=%SUCCESS%+%errorlevel%

exit ${SUCCESS}