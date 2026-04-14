@echo off
setlocal
python "%~dp0find_references_by_guid.py" %*
exit /b %errorlevel%
