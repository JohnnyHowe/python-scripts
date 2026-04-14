@echo off
setlocal
python "%~dp0remove_tracked_files_in_gitignore.py" %*
exit /b %errorlevel%
