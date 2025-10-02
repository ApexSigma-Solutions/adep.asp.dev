# Setup Safe-Delete for PowerShell

This document provides instructions on how to set up the safe-delete function for PowerShell, which overrides the standard `Remove-Item` command to prevent accidental permanent deletion of files.

## 1. Locate your PowerShell profile

You can find the path to your PowerShell profile by running the following command in your PowerShell terminal:

```powershell
$PROFILE
```

If the file does not exist, you can create it by running:

```powershell
New-Item -Path $PROFILE -Type File -Force
```

## 2. Add the following lines to your profile

Open your PowerShell profile file in a text editor and add the following lines. Make sure to replace `C:\path\to\your\project` with the absolute path to the `ApexSigmaProjects.Dev` directory.

```powershell
# ApexSigma Safe-Delete
$apexSigmaProjectRoot = "C:\path\to\your\project"
$safeDeleteScript = Join-Path -Path $apexSigmaProjectRoot -ChildPath "scripts\utils\safe-delete.ps1"

if (Test-Path -Path $safeDeleteScript) {
    Import-Module $safeDeleteScript
    Set-Alias -Name rm -Value Safe-RemoveItem -Option AllScope -Force
    Set-Alias -Name del -Value Safe-RemoveItem -Option AllScope -Force
    Set-Alias -Name rmdir -Value Safe-RemoveItem -Option AllScope -Force
}
```

## 3. Reload your PowerShell profile

For the changes to take effect, you need to reload your PowerShell profile. You can do this by running the following command in your terminal:

```powershell
. $PROFILE
```

## 4. Verify the setup

To verify that the safe-delete function is working correctly, you can create a test file and then try to remove it.

```powershell
# Create a test file
New-Item -ItemType File -Name "test_file.txt" | Out-Null

# Try to remove it
Remove-Item .\test_file.txt
```

You should see a message indicating that the file has been moved to the trash directory. You can also check the contents of the `_archive/trash` directory to confirm that the file is there.

