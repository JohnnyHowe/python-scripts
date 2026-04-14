@echo off
setlocal
python "%~dp0generate_bat_wrappers.py" %*
exit /b %errorlevel%
