@echo off
setlocal
python "%~dp0check_gh_auth.py" %*
exit /b %errorlevel%
