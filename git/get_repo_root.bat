@echo off
setlocal
python "%~dp0get_repo_root.py" %*
exit /b %errorlevel%
