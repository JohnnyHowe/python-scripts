@echo off
setlocal
python "%~dp0get_all_branches.py" %*
exit /b %errorlevel%
