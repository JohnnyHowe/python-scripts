@echo off
setlocal
python "%~dp0delete_branches_already_merged.py" %*
exit /b %errorlevel%
