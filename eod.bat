@echo off
REM EOD (End of Day) Command Protocol - Windows Batch Script
REM Mandatory standardized procedure for capturing development progress

echo ================================================================================
echo                      EOD (END OF DAY) COMMAND PROTOCOL                          
echo ================================================================================
echo.
echo Mandatory standardized procedure for capturing development progress and 
echo ingesting into the ApexSigma knowledge graph.
echo.

REM Change to the ApexSigma directory
cd /d "%~dp0"

REM Run the EOD command script
python eod.py %*

REM Check exit code and provide feedback
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] EOD protocol completed successfully!
    echo Your development progress has been captured and ingested into the knowledge graph.
    echo.
) else (
    echo.
    echo [ERROR] EOD protocol failed!
    echo Check the output above for details on what went wrong.
    echo.
    echo Common issues:
    echo   - Uncommitted changes in git working directory
    echo   - InGest-LLM service not running ^(port 8000^)
    echo   - Test failures preventing completion
    echo.
)

pause