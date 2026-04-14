@echo off
setlocal
python "%~dp0delete_all_cache.py" %*
exit /b %errorlevel%
