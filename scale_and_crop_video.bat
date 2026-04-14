@echo off
setlocal
python "%~dp0scale_and_crop_video.py" %*
exit /b %errorlevel%
