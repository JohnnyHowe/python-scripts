@echo off
setlocal
python "%~dp0print_table.py" %*
exit /b %errorlevel%
