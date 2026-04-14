@echo off
setlocal
python "%~dp0json_tidier.py" %*
exit /b %errorlevel%
