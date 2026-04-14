@echo off
setlocal
python "%~dp0normalize_audio.py" %*
exit /b %errorlevel%
