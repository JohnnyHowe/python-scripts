@echo off
setlocal
python "%~dp0git_script_config.py" %*
exit /b %errorlevel%
