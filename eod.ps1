# EOD (End of Day) Command Protocol - PowerShell Script
# Mandatory standardized procedure for capturing development progress

param(
    [string]$Project,
    [switch]$SkipTests,
    [switch]$DryRun,
    [switch]$Help
)

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "                     EOD (END OF DAY) COMMAND PROTOCOL                         " -ForegroundColor Cyan  
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Mandatory standardized procedure for capturing development progress" -ForegroundColor Yellow
Write-Host "and ingesting into the ApexSigma knowledge graph." -ForegroundColor Yellow
Write-Host ""

# Change to the ApexSigma root directory
Push-Location $ScriptDir

try {
    # Build arguments for Python script
    $args = @()
    if ($Project) { $args += "--project"; $args += $Project }
    if ($SkipTests) { $args += "--skip-tests" }
    if ($DryRun) { $args += "--dry-run" }
    if ($Help) { $args += "--help" }
    
    # Run the EOD command script
    $result = & python eod.py @args
    $exitCode = $LASTEXITCODE
    
    Write-Host ""
    if ($exitCode -eq 0) {
        Write-Host "[SUCCESS] EOD protocol completed successfully!" -ForegroundColor Green
        Write-Host "Your development progress has been captured and ingested into the knowledge graph." -ForegroundColor Green
        Write-Host ""
    } else {
        Write-Host "[ERROR] EOD protocol failed!" -ForegroundColor Red
        Write-Host "Check the output above for details on what went wrong." -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Common issues:" -ForegroundColor Yellow
        Write-Host "  - Uncommitted changes in git working directory" -ForegroundColor White
        Write-Host "  - InGest-LLM service not running (port 8000)" -ForegroundColor White
        Write-Host "  - Test failures preventing completion" -ForegroundColor White
        Write-Host ""
    }
    
    exit $exitCode
}
finally {
    # Always return to original directory
    Pop-Location
}