@echo off
setlocal EnableExtensions
cd /d "%~dp0..\.."
set "TITLE=SkyFlies Workshop - Step 1: repo bootstrap"

if /I "%~1"=="--here" goto :run

start "%TITLE%" cmd /k "%~f0" --here
exit /b 0

:run
title %TITLE%
echo.
echo  Opening Step 1 in this window. Leave it open until Done.
echo.

set "PY="
where py >nul 2>&1
if not errorlevel 1 (
  py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3,11) else 1)" >nul 2>&1
  if not errorlevel 1 set "PY=py -3"
)
if not defined PY (
  where python >nul 2>&1
  if not errorlevel 1 set "PY=python"
)
if not defined PY (
  echo  [fail] Python 3.11+ not on PATH.
  echo  Install from https://www.python.org/downloads/ and tick Add python.exe to PATH.
  echo.
  pause
  exit /b 1
)

%PY% workshop\_lib\step_runner.py --step 01
set "ERR=%ERRORLEVEL%"
echo.
if not "%ERR%"=="0" (
  echo  Step 1 failed. Scroll up, fix, then run this .bat again.
)
pause
exit /b %ERR%
