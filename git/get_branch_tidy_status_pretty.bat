@echo off
setlocal
python "%~dp0get_branch_tidy_status_pretty.py" %*
exit /b %errorlevel%
