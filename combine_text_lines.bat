@echo off
setlocal
python "%~dp0combine_text_lines.py" %*
exit /b %errorlevel%
