# Setup EOD Command for PowerShell
# Run this script once to enable the EOD command from anywhere

Write-Host "Setting up EOD (End of Day) command..." -ForegroundColor Cyan

# Get the current directory (ApexSigma root)
$ApexSigmaDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "ApexSigma Directory: $ApexSigmaDir" -ForegroundColor Yellow

# Function definition
$functionDef = @"
function eod {
    param(
        [string]`$Project,
        [switch]`$SkipTests,
        [switch]`$DryRun,
        [switch]`$Help
    )
    
    `$currentLocation = Get-Location
    try {
        Set-Location "$ApexSigmaDir"
        
        `$args = @()
        if (`$Project) { `$args += "--project"; `$args += `$Project }
        if (`$SkipTests) { `$args += "--skip-tests" }
        if (`$DryRun) { `$args += "--dry-run" }
        if (`$Help) { `$args += "--help" }
        
        Write-Host "================================================================================
                     EOD (END OF DAY) COMMAND PROTOCOL                         
================================================================================" -ForegroundColor Cyan
        Write-Host "Mandatory standardized procedure for capturing development progress" -ForegroundColor Yellow
        Write-Host ""
        python eod.py @args
    }
    finally {
        Set-Location `$currentLocation
    }
}

# Alias for /command eod
Set-Alias -Name '/command' -Value eod -Force

# Function for /command eod specifically
function Invoke-CommandEod {
    param([string]`$Command)
    if (`$Command -eq "eod") {
        eod
    } else {
        Write-Host "Unknown command: `$Command" -ForegroundColor Red
        Write-Host "Available commands: eod" -ForegroundColor Yellow
    }
}

# Set up the /command alias to work with parameters
function global:command {
    param([Parameter(Position=0)][string]`$SubCommand)
    if (`$SubCommand -eq "eod") {
        eod @args[1..(`$args.Length-1)]
    } else {
        Write-Host "Unknown command: `$SubCommand" -ForegroundColor Red
        Write-Host "Available commands: eod" -ForegroundColor Yellow
    }
}
"@

# Check if profile exists, create if not
if (!(Test-Path $PROFILE)) {
    Write-Host "Creating PowerShell profile at: $PROFILE" -ForegroundColor Green
    New-Item -ItemType File -Path $PROFILE -Force | Out-Null
}

# Add the function to profile
Write-Host "Adding EOD function to PowerShell profile..." -ForegroundColor Green
Add-Content -Path $PROFILE -Value "`n# EOD (End of Day) Command Protocol"
Add-Content -Path $PROFILE -Value $functionDef

Write-Host "`nEOD command setup complete!" -ForegroundColor Green
Write-Host "`nTo activate in this session, run:" -ForegroundColor Yellow
Write-Host ". `$PROFILE" -ForegroundColor White
Write-Host "`nOr restart PowerShell." -ForegroundColor Yellow

Write-Host "`nUsage examples:" -ForegroundColor Yellow
Write-Host "  eod                        # Basic EOD protocol" -ForegroundColor White
Write-Host "  eod -SkipTests             # Skip running tests" -ForegroundColor White  
Write-Host "  eod -DryRun                # Test run without submission" -ForegroundColor White
Write-Host "  eod -Project devenviro.as  # Specify project" -ForegroundColor White
Write-Host "  command eod                # Using /command alias" -ForegroundColor White