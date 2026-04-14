@echo off
setlocal
python "%~dp0get_all_non_snake_case_files.py" %*
exit /b %errorlevel%
