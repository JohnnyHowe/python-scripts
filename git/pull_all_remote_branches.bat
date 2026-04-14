@echo off
setlocal
python "%~dp0pull_all_remote_branches.py" %*
exit /b %errorlevel%
