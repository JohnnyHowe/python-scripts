@echo off
setlocal
python "%~dp0has_merge_conflicts.py" %*
exit /b %errorlevel%
