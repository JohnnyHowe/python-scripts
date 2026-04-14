@echo off
setlocal
python "%~dp0generate_scripts_index.py" %*
exit /b %errorlevel%
