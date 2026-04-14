@echo off
setlocal
python "%~dp0godot_delete_redunant_import_files.py" %*
exit /b %errorlevel%
