@echo off
setlocal
python "%~dp0get_branches_already_merged.py" %*
exit /b %errorlevel%
