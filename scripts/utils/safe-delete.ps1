# safe-delete.ps1
#
# This script provides a safe alternative to the 'Remove-Item' command by moving
# files to a trash directory instead of permanently deleting them.

function Safe-RemoveItem {
    [CmdletBinding(SupportsShouldProcess=$true)]
    param(
        [Parameter(Mandatory=$true, Position=0, ValueFromPipeline=$true, ValueFromPipelineByPropertyName=$true)]
        [string[]]$Path
    )

    begin {
        $trashDir = Join-Path -Path (git rev-parse --show-toplevel) -ChildPath "_archive\trash"
        if (-not (Test-Path -Path $trashDir)) {
            New-Item -ItemType Directory -Path $trashDir -Force | Out-Null
        }
    }

    process {
        foreach ($item in $Path) {
            if (Test-Path -Path $item) {
                if ($pscmdlet.ShouldProcess($item, "Move to Trash")) {
                    $timestamp = Get-Date -Format "yyyyMMddHHmmss"
                    $baseName = (Get-Item -Path $item).Name
                    $destination = Join-Path -Path $trashDir -ChildPath "${baseName}_${timestamp}"
                    Move-Item -Path $item -Destination $destination -Force
                    Write-Host "Moved '$item' to trash."
                }
            } else {
                Write-Error "safe_rm: cannot remove '$item': No such file or directory"
            }
        }
    }
}

# To use this, add the following to your PowerShell profile ($PROFILE):
#
# Import-Module /path/to/your/project/scripts/utils/safe-delete.ps1
# Set-Alias -Name rm -Value Safe-RemoveItem -Option AllScope
# Set-Alias -Name del -Value Safe-RemoveItem -Option AllScope
# Set-Alias -Name rmdir -Value Safe-RemoveItem -Option AllScope
