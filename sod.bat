@echo off
REM Society of Agents Deploy (SOD) - Windows Batch Script
REM This script provides a convenient /sod command for Windows users

echo ==============================================================================
echo                      SOCIETY OF AGENTS DEPLOY (SOD)                          
echo ==============================================================================

REM Change to the ApexSigma directory
cd /d "%~dp0"

REM Run the SOD deployment script
python sod.py %*

REM Check exit code and provide feedback
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] Society of Agents deployment completed successfully!
    echo.
    echo Dashboard Links:
    echo   * DevEnviro API: http://localhost:8090/docs
    echo   * Grafana:       http://localhost:8080 ^(admin/apexsigma123^)
    echo   * Prometheus:    http://localhost:9090  
    echo   * Jaeger:        http://localhost:16686
    echo   * RabbitMQ:      http://localhost:15672
    echo.
) else (
    echo.
    echo [ERROR] Society of Agents deployment failed!
    echo Check the logs above for details.
    echo.
    echo Common fixes:
    echo   - Ensure Docker Desktop is running
    echo   - Run: sod --force ^(to clean up existing containers^)
    echo   - Check .env files in each project directory
    echo.
)

pause