@echo off
setlocal
python "%~dp0image_color_to_alpha.py" %*
exit /b %errorlevel%
