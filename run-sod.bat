@echo off
echo ================================================================================
echo                      SOCIETY OF AGENTS DEPLOY (SOD)                          
echo ================================================================================
echo.

REM Change to the ApexSigma directory (where this batch file is located)
cd /d "%~dp0"

REM Run the SOD deployment script with any passed arguments
python sod.py %*

echo.
echo ================================================================================
pause