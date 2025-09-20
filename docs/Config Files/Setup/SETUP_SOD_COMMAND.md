# Setup SOD Command - Make /sod Available Anywhere

To use the `/sod` command from any directory, choose one of these setup methods:

## Method 1: PowerShell Function (Recommended for Windows)

Add this function to your PowerShell profile:

1. Open PowerShell as Administrator
2. Edit your profile: `notepad $PROFILE` 
3. Add this function:

```powershell
function sod {
    param(
        [switch]$Force,
        [switch]$SkipAudit,
        [switch]$Verbose,
        [switch]$Help
    )
    
    $currentLocation = Get-Location
    try {
        Set-Location "C:\Users\steyn\ApexSigmaProjects.Dev"
        
        $args = @()
        if ($Force) { $args += "--force" }
        if ($SkipAudit) { $args += "--skip-audit" }
        if ($Verbose) { $args += "--verbose" }
        if ($Help) { $args += "--help" }
        
        python sod.py @args
    }
    finally {
        Set-Location $currentLocation
    }
}
```

4. Reload profile: `. $PROFILE`

**Usage:**
```powershell
sod                    # Basic deployment
sod -Force            # Force cleanup
sod -Verbose          # Verbose logging
sod -Force -Verbose   # Force + verbose
```

## Method 2: Environment Variable (Cross-Platform)

Add the ApexSigma directory to your PATH:

### Windows
```cmd
setx PATH "%PATH%;C:\Users\steyn\ApexSigmaProjects.Dev"
```

### Linux/macOS
```bash
echo 'export PATH="$PATH:/path/to/ApexSigmaProjects.Dev"' >> ~/.bashrc
source ~/.bashrc
```

**Usage:**
```bash
python sod.py --force --verbose
```

## Method 3: Direct Script Execution

From the ApexSigma root directory:

### Windows PowerShell
```powershell
cd C:\Users\steyn\ApexSigmaProjects.Dev
.\sod.ps1 -Force -Verbose
```

### Windows Command Prompt
```cmd
cd C:\Users\steyn\ApexSigmaProjects.Dev
sod.bat --force --verbose
```

### Python (Any OS)
```bash
cd /path/to/ApexSigmaProjects.Dev
python sod.py --force --verbose
```

## Quick Test

After setup, test the command:

```powershell
sod -Help
```

You should see the SOD help output with available options.

## Troubleshooting

### "sod is not recognized"
- Ensure you've reloaded your PowerShell profile: `. $PROFILE`
- Check the path in the function matches your actual directory
- Verify Python is in your PATH: `python --version`

### "Permission denied" or execution policy issues
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Docker not found
- Ensure Docker Desktop is running
- Verify docker command works: `docker --version`

Once configured, you can run `sod` from any directory to deploy the complete ApexSigma Society of Agents ecosystem!