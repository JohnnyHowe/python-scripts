@echo off
setlocal
python "%~dp0get_changelog.py" %*
exit /b %errorlevel%
