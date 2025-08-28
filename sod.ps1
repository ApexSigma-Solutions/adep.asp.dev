# Society of Agents Deploy (SOD) - PowerShell Script
# This script can be called from anywhere and will change to the correct directory

param(
    [switch]$Force,
    [switch]$SkipAudit, 
    [switch]$Verbose,
    [switch]$Help
)

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "                      SOCIETY OF AGENTS DEPLOY (SOD)                           " -ForegroundColor Cyan  
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Change to the ApexSigma root directory
Push-Location $ScriptDir

try {
    # Build arguments for Python script
    $args = @()
    if ($Force) { $args += "--force" }
    if ($SkipAudit) { $args += "--skip-audit" }  
    if ($Verbose) { $args += "--verbose" }
    if ($Help) { $args += "--help" }
    
    # Run the SOD deployment script
    $result = & python sod.py @args
    $exitCode = $LASTEXITCODE
    
    Write-Host ""
    if ($exitCode -eq 0) {
        Write-Host "[SUCCESS] Society of Agents deployment completed successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Dashboard Links:" -ForegroundColor Yellow
        Write-Host "  * DevEnviro API: http://localhost:8090/docs" -ForegroundColor White
        Write-Host "  * Grafana:       http://localhost:8080 (admin/apexsigma123)" -ForegroundColor White
        Write-Host "  * Prometheus:    http://localhost:9090" -ForegroundColor White  
        Write-Host "  * Jaeger:        http://localhost:16686" -ForegroundColor White
        Write-Host "  * RabbitMQ:      http://localhost:15672" -ForegroundColor White
        Write-Host ""
    } else {
        Write-Host "[ERROR] Society of Agents deployment failed!" -ForegroundColor Red
        Write-Host "Check the logs above for details." -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Common fixes:" -ForegroundColor Yellow
        Write-Host "  - Ensure Docker Desktop is running" -ForegroundColor White
        Write-Host "  - Run: .\sod.ps1 -Force (to clean up existing containers)" -ForegroundColor White
        Write-Host "  - Check .env files in each project directory" -ForegroundColor White
        Write-Host ""
    }
    
    exit $exitCode
}
finally {
    # Always return to original directory
    Pop-Location
}