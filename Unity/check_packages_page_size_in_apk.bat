@echo off
setlocal
python "%~dp0check_packages_page_size_in_apk.py" %*
exit /b %errorlevel%
