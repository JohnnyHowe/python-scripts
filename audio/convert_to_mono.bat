@echo off
setlocal
python "%~dp0convert_to_mono.py" %*
exit /b %errorlevel%
