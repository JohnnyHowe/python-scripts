@echo off
setlocal
python "%~dp0get_branch_tidy_status.py" %*
exit /b %errorlevel%
