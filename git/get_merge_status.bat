@echo off
setlocal
python "%~dp0get_merge_status.py" %*
exit /b %errorlevel%
