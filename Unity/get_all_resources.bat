@echo off
setlocal
python "%~dp0get_all_resources.py" %*
exit /b %errorlevel%
