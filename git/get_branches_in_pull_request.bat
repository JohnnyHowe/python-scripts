@echo off
setlocal
python "%~dp0get_branches_in_pull_request.py" %*
exit /b %errorlevel%
