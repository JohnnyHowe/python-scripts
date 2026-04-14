@echo off
setlocal
python "%~dp0count_lines.py" %*
exit /b %errorlevel%
