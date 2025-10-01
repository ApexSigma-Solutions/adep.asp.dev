# Session Management Commands for ApexSigma Development

param(
    [Parameter(Mandatory=$false)]
    [string]$Command,
    
    [Parameter(Mandatory=$false)]
    [string]$SessionId,
    
    [Parameter(Mandatory=$false)]
    [string]$Goals,
    
    [Parameter(Mandatory=$false)]
    [string]$Completed,
    
    [Parameter(Mandatory=$false)]
    [string]$Status,
    
    [Parameter(Mandatory=$false)]
    [string]$Challenges,
    
    [Parameter(Mandatory=$false)]
    [string]$Next,
    
    [Parameter(Mandatory=$false)]
    [string]$Summary
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonScript = Join-Path $ScriptDir "session_manager.py"

if ($Command -eq "start") {
    python $PythonScript start --goals $Goals
} 
elseif ($Command -eq "progress") {
    python $PythonScript progress --session-id $SessionId --completed $Completed --status $Status --challenges $Challenges --next $Next
} 
elseif ($Command -eq "complete") {
    python $PythonScript complete --session-id $SessionId --summary $Summary
} 
elseif ($Command -eq "list") {
    python $PythonScript list
} 
elseif ($Command -eq "show") {
    python $PythonScript show --session-id $SessionId
} 
else {
    Write-Host "Usage:"
    Write-Host "  session.ps1 start [goals] - Start a new session"
    Write-Host "  session.ps1 progress <session-id> <completed> <status> <challenges> <next> - Log progress"
    Write-Host "  session.ps1 complete <session-id> [summary] - Complete a session"
    Write-Host "  session.ps1 list - List all sessions"
    Write-Host "  session.ps1 show <session-id> - Show session details"
}