@echo off
setlocal
python "%~dp0get_push_status.py" %*
exit /b %errorlevel%
