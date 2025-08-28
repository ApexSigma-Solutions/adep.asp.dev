# Setup SOD Command for PowerShell
# Run this script once to enable the /sod command from anywhere

Write-Host "Setting up SOD (Society of Agents Deploy) command..." -ForegroundColor Cyan

# Get the current directory (ApexSigma root)
$ApexSigmaDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "ApexSigma Directory: $ApexSigmaDir" -ForegroundColor Yellow

# Function definition
$functionDef = @"
function sod {
    param(
        [switch]`$Force,
        [switch]`$SkipAudit,
        [switch]`$Verbose,
        [switch]`$Help
    )
    
    `$currentLocation = Get-Location
    try {
        Set-Location "$ApexSigmaDir"
        
        `$args = @()
        if (`$Force) { `$args += "--force" }
        if (`$SkipAudit) { `$args += "--skip-audit" }
        if (`$Verbose) { `$args += "--verbose" }
        if (`$Help) { `$args += "--help" }
        
        Write-Host "Society of Agents Deploy (SOD)" -ForegroundColor Cyan
        Write-Host "==============================" -ForegroundColor Cyan
        python sod.py @args
    }
    finally {
        Set-Location `$currentLocation
    }
}

# Alias for /sod
Set-Alias -Name '/sod' -Value sod -Force
"@

# Check if profile exists, create if not
if (!(Test-Path $PROFILE)) {
    Write-Host "Creating PowerShell profile at: $PROFILE" -ForegroundColor Green
    New-Item -ItemType File -Path $PROFILE -Force | Out-Null
}

# Add the function to profile
Write-Host "Adding SOD function to PowerShell profile..." -ForegroundColor Green
Add-Content -Path $PROFILE -Value "`n# SOD (Society of Agents Deploy) Command"
Add-Content -Path $PROFILE -Value $functionDef

Write-Host "`nSOD command setup complete!" -ForegroundColor Green
Write-Host "`nTo activate in this session, run:" -ForegroundColor Yellow
Write-Host ". `$PROFILE" -ForegroundColor White
Write-Host "`nOr restart PowerShell." -ForegroundColor Yellow

Write-Host "`nUsage examples:" -ForegroundColor Yellow
Write-Host "  sod                 # Basic deployment" -ForegroundColor White
Write-Host "  sod -Force          # Force cleanup + deploy" -ForegroundColor White  
Write-Host "  sod -Verbose        # Verbose logging" -ForegroundColor White
Write-Host "  sod -Help           # Show help" -ForegroundColor White
Write-Host "  /sod -Force         # Using alias" -ForegroundColor White