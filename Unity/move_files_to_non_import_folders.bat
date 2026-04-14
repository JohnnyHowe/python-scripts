@echo off
setlocal
python "%~dp0move_files_to_non_import_folders.py" %*
exit /b %errorlevel%
