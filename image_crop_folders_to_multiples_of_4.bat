@echo off
setlocal
python "%~dp0image_crop_folders_to_multiples_of_4.py" %*
exit /b %errorlevel%
