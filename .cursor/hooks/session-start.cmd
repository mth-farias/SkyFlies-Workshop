@echo off
REM Fallback Cursor hook launcher when `python` is not on PATH.
py -3 "%~dp0session-start.py" %*
if errorlevel 1 python "%~dp0session-start.py" %*
