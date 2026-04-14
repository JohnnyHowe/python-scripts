@echo off
setlocal
python "%~dp0ensure_github_cli_is_authenticated.py" %*
exit /b %errorlevel%
