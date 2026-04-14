@echo off
setlocal
python "%~dp0convert_video_to_gif.py" %*
exit /b %errorlevel%
