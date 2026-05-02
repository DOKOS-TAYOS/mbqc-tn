@echo off
setlocal
set "VENV_PYTHON=%~dp0..\.venv\Scripts\python.exe"
if exist "%VENV_PYTHON%" (
    "%VENV_PYTHON%" "%~dp0..\scripts\run_template_command.py" clean %*
) else (
    python "%~dp0..\scripts\run_template_command.py" clean %*
)
exit /b %errorlevel%
