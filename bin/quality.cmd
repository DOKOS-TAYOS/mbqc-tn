@echo off
setlocal
set "VENV_PYTHON=%~dp0..\.venv\Scripts\python.exe"
if exist "%VENV_PYTHON%" (
    "%VENV_PYTHON%" "%~dp0..\scripts\run_template_command.py" quality %*
) else (
    python "%~dp0..\scripts\run_template_command.py" quality %*
)
exit /b %errorlevel%
