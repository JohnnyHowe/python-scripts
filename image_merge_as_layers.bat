@echo off
setlocal
python "%~dp0image_merge_as_layers.py" %*
exit /b %errorlevel%
