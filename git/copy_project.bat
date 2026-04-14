@echo off
setlocal
python "%~dp0copy_project.py" %*
exit /b %errorlevel%
