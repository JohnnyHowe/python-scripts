@echo off
setlocal
python "%~dp0create_utility_folder_index.py" %*
exit /b %errorlevel%
