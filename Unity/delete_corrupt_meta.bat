@echo off
setlocal
python "%~dp0delete_corrupt_meta.py" %*
exit /b %errorlevel%
