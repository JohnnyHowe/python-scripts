@echo off
setlocal
python "%~dp0image_crop_to_content.py" %*
exit /b %errorlevel%
