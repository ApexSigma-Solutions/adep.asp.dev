---
aliases:
  - 20+ Years of Google Photos, 100GB of Files, One PowerShell Script
---



I had posted this earlier, but wasn't satisfied with the contents of the body. What follows is the message I should have given to clearly explain a problem I was trying to solve. What follows is my story.

I recently downloaded 100 GB of media files from my Google Drive. Since the files dated back over twenty years, I had to use their Google Takeout service. It packaged all of my files into fifty separate 2 GB zipped files. It was a pain to download all of them, and the process worsened after unzipping them.

The folder structure is the zipped folder as the root. Under that is another individual folder for Takeout. The next subfolder is Google Photos. As you enter that folder, you'll find many folders organized by year. As you enter each folder, you'll find all the media file types that you've been storing over the years. Among them are dozens of JSON files. I initiated a manual process of sorting by file type, selecting all JSON files, deleting them, and then moving all the remaining files to a single folder for media storage.

While this manual process worked, I found that as I transitioned from one set of uncompressed folders to another and moved the files out, numerous duplicate name conflicts arose. I needed to automate the renaming of each file.

I'm no expert in PowerShell, but I've come to utilize AI to help create simple scripts that automate redundant administrative tasks. The first script I received help with was to traverse all subfolders and delete all JSON files recursively. That was easy.

Next, I went about renaming files. I wanted to use the Date and Time that the file was created. However, not all of my files had that information in their metadata, as shown by the file property details. After further investigation, I discovered a third-party command-line tool called ExifTool. Once I downloaded and configured that, I found that the metadata I wanted to look for was an attribute called DateTimeOriginal. However, I also discovered that many of my older files lacked that information and were effectively blank. So, I had to come up with a way to rename them without causing conflict. I asked AI to randomly generate an eight-character name using uppercase letters and numbers 0-9. For the majority of files, I used a standard naming convention of YYYY-MM-DD\_HH-MM\_HX.fileType. Obviously, that was for Year, Month, Hour, Minute, and two HEX characters, which I had randomly generated. I asked AI to help me set up this script to go through a folder and rename all media files recursively. It worked great.

As I worked through more file renaming and consolidating, I realized I needed another folder to store all subfolder media files, rename them, and then move them to a final media folder. That was to avoid constantly renaming files that were already renamed. Once all media files in the temporary folder have been renamed, the script moves them to the final media storage folder.

As I developed what was initially three scripts, I reached a point where I felt confident that they were working smoothly. I then asked AI to help stitch them all together and provide a GUI for all steps, including a progress window for each one. This part became an iterative exercise, as it required addressing numerous errors and warnings. Ultimately, it all came together. After multiple tests on the downloaded Google media, it appears to be an effective script. It may not be the most elegant, but I'm happy to share it with this community. This script works with any Windows folder structure and is not limited to just Google media file exports.

That holistic media move/rename/store script follows:

**EDIT: I realized after the fact that I also wanted to log file size in its proper format. So, I updated the script to capture that information for the CVS log as well. That component is in this updated script below.**

    # ============================================
    # MASTER MEDIA FILE ORGANIZATION SCRIPT
    # ============================================
    
    # This script requires that ExifTool by Phil Harvey is on your computer and it's referenced in your enviornmental variables System PATH.
    # You can download ExifTool at: https://exiftool.org/
    # See https://exiftool.org/install.html for more installation instructions.
    # Once installed, test it by running PowerShell and typing exiftool, and hit Enter. If it runs, you're golden!
    
    function Show-ProgressWindow {
        param (
            [string]$Title,
            [string]$TaskName,
            [int]$Total
        )
    
        Add-Type -AssemblyName System.Windows.Forms
    
        $form = New-Object System.Windows.Forms.Form
        $form.Text = $Title
        $form.Width = 400
        $form.Height = 100
        $form.StartPosition = "CenterScreen"
    
        $label = New-Object System.Windows.Forms.Label
        $label.Text = $TaskName
        $label.AutoSize = $true
        $label.Top = 10
        $label.Left = 10
        $form.Controls.Add($label)
    
        $progressBar = New-Object System.Windows.Forms.ProgressBar
        $progressBar.Minimum = 0
        $progressBar.Maximum = $Total
        $progressBar.Value = 0
        $progressBar.Width = 360
        $progressBar.Height = 20
        $progressBar.Left = 10
        $progressBar.Top = 30
        $form.Controls.Add($progressBar)
    
        $form.Show()
        return @{ Form = $form; ProgressBar = $progressBar }
    }
    
    Add-Type -AssemblyName System.Windows.Forms
    $folderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
    
    # GUI Folder Selections
    $folderBrowser.Description = "Select the folder where your original media files are located"
    $null = $folderBrowser.ShowDialog()
    $sourcePath = $folderBrowser.SelectedPath
    
    $folderBrowser.Description = "Select the folder to stage files for renaming"
    $null = $folderBrowser.ShowDialog()
    $stagingPath = $folderBrowser.SelectedPath
    
    $folderBrowser.Description = "Select the final folder to store renamed files"
    $null = $folderBrowser.ShowDialog()
    $finalPath = $folderBrowser.SelectedPath
    
    foreach ($path in @($sourcePath, $stagingPath, $finalPath)) {
        if (-not (Test-Path $path)) {
            New-Item -ItemType Directory -Path $path | Out-Null
        }
    }
    
    # JSON Deletion Confirmation
    $dialogResult = [System.Windows.Forms.MessageBox]::Show(
        "Do you want to delete all .JSON files in the source folder?",
        "Delete JSON Files?",
        [System.Windows.Forms.MessageBoxButtons]::YesNo,
        [System.Windows.Forms.MessageBoxIcon]::Question
    )
    
    if ($dialogResult -eq [System.Windows.Forms.DialogResult]::Yes) {
        try {
            $jsonFiles = Get-ChildItem -Path $sourcePath -Recurse -Filter *.json
            $progress = Show-ProgressWindow -Title "Deleting JSON Files" -TaskName "Cleaning up .json files..." -Total $jsonFiles.Count
            $count = 0
            foreach ($file in $jsonFiles) {
                Remove-Item -Path $file.FullName -Force
                $count++
                $progress.ProgressBar.Value = $count
                [System.Windows.Forms.Application]::DoEvents()
            }
            Start-Sleep -Milliseconds 500
            $progress.Form.Close()
            Write-Host "All .json files have been deleted."
        } catch {
            Write-Host "Error while deleting .json files: $_"
        }
    } else {
        Write-Host "Skipping JSON cleanup..."
    }
    
    # Define media extensions
    $mediaExtensions = @(
        "*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp", "*.tif", "*.tiff", "*.webp",
        "*.heic", "*.raw", "*.cr2", "*.nef", "*.orf", "*.arw", "*.dng", "*.rw2", "*.pef", "*.sr2",
        "*.mp4", "*.mov", "*.avi", "*.mkv", "*.wmv", "*.flv", "*.3gp", "*.webm",
        "*.mts", "*.m2ts", "*.ts", "*.vob", "*.mpg", "*.mpeg"
    )
    
    # Mass move media files
    $filesToMove = @()
    foreach ($ext in $mediaExtensions) {
        $filesToMove += Get-ChildItem -Path $sourcePath -Filter $ext -Recurse
    }
    $progress = Show-ProgressWindow -Title "Mass Move" -TaskName "Moving files to staging folder..." -Total $filesToMove.Count
    $count = 0
    foreach ($file in $filesToMove) {
        Move-Item -Path $file.FullName -Destination (Join-Path $stagingPath $file.Name) -Force
        $count++
        $progress.ProgressBar.Value = $count
        [System.Windows.Forms.Application]::DoEvents()
    }
    Start-Sleep -Milliseconds 500
    $progress.Form.Close()
    
    # Function to generate random names
    function Get-RandomName {
        $chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        -join ((1..8) | ForEach-Object { $chars[(Get-Random -Minimum 0 -Maximum $chars.Length)] })
    }
    
    # Function to get readable file size
    function Get-ReadableFileSize($size) {
        if ($size -ge 1GB) {
            return "{0:N2} GB" -f ($size / 1GB)
        } elseif ($size -ge 1MB) {
            return "{0:N2} MB" -f ($size / 1MB)
        } else {
            return "{0:N2} KB" -f ($size / 1KB)
        }
    }
    
    # Rename files using DateTimeOriginal or random fallback
    $timestampTracker = @{}
    $global:LogOutput = @()
    $global:logPrefix = (Get-Date -Format "yyyy-MM-dd_HH-mm")
    $renameTargets = @()
    foreach ($ext in $mediaExtensions) {
        $renameTargets += Get-ChildItem -Path $stagingPath -Filter $ext -Recurse
    }
    $progress = Show-ProgressWindow -Title "Renaming Files" -TaskName "Renaming files..." -Total $renameTargets.Count
    $count = 0
    foreach ($file in $renameTargets) {
        $ext = $file.Extension.ToLower()
        $dateRaw = & exiftool -q -q -DateTimeOriginal -s3 "$($file.FullName)"
        $fileSizeReadable = Get-ReadableFileSize $file.Length
    
        if ($dateRaw) {
            try {
                $dt = [datetime]::ParseExact($dateRaw, "yyyy:MM:dd HH:mm:ss", $null)
                $timestampKey = $dt.ToString("yyyy-MM-dd_HH-mm")
                if (-not $timestampTracker.ContainsKey($timestampKey)) {
                    $timestampTracker[$timestampKey] = 0
                } else {
                    $timestampTracker[$timestampKey] += 1
                }
                $hexSuffix = "{0:X2}" -f (Get-Random -Minimum 0 -Maximum 256)
                $newName = "$timestampKey" + "_$hexSuffix$ext"
                $collisionPath = Join-Path $file.DirectoryName $newName
                while (Test-Path $collisionPath) {
                    $randomTag = Get-Random -Minimum 1000 -Maximum 9999
                    $newName = $newName.Replace($ext, "_$randomTag$ext")
                    $collisionPath = Join-Path $file.DirectoryName $newName
                }
                Rename-Item -Path $file.FullName -NewName $newName
                $global:LogOutput += [PSCustomObject]@{
                    Timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
                    Action = "Renamed (Conflict Resolved)"
                    OriginalName = $file.Name
                    NewName = $newName
                    OriginalFilePath = $file.DirectoryName
                    FinalFilePath = $finalPath
                    FileSize = $fileSizeReadable
                    RenameType = "Random-Conflict"
                }
                $global:LogOutput += [PSCustomObject]@{
                    Timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
                    Action = "Renamed"
                    OriginalName = $file.Name
                    NewName = $newName
                    OriginalFilePath = $file.DirectoryName
                    FinalFilePath = $finalPath
                    FileSize = $fileSizeReadable
                    RenameType = "Metadata"
                }
            } catch {}
        } else {
            do {
                $randomName = Get-RandomName
                $newName = "$randomName$ext"
                $newPath = Join-Path $stagingPath $newName
            } while (Test-Path $newPath)
    
            $collisionPath = Join-Path $file.DirectoryName $newName
            while (Test-Path $collisionPath) {
                $randomTag = Get-Random -Minimum 1000 -Maximum 9999
                $newName = $newName.Replace($ext, "_$randomTag$ext")
                $collisionPath = Join-Path $file.DirectoryName $newName
            }
            Rename-Item -Path $file.FullName -NewName $newName
            $global:LogOutput += [PSCustomObject]@{
                Timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
                Action = "Renamed (Conflict Resolved)"
                OriginalName = $file.Name
                NewName = $newName
                OriginalFilePath = $file.DirectoryName
                FinalFilePath = $finalPath
                FileSize = $fileSizeReadable
                RenameType = "Random-Conflict"
            }
            $global:LogOutput += [PSCustomObject]@{
                Timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
                Action = "Renamed"
                OriginalName = $file.Name
                NewName = $newName
                OriginalFilePath = $file.DirectoryName
                FinalFilePath = $finalPath
                FileSize = $fileSizeReadable
                RenameType = "Random"
            }
        }
        $count++
        $progress.ProgressBar.Value = $count
        [System.Windows.Forms.Application]::DoEvents()
    }
    Start-Sleep -Milliseconds 500
    $progress.Form.Close()
    
    # Final move
    $finalFiles = @()
    foreach ($ext in $mediaExtensions) {
        $finalFiles += Get-ChildItem -Path $stagingPath -Filter $ext -Recurse
    }
    $progress = Show-ProgressWindow -Title "Final Move" -TaskName "Moving renamed files to final folder..." -Total $finalFiles.Count
    $count = 0
    foreach ($file in $finalFiles) {
        Move-Item -Path $file.FullName -Destination (Join-Path $finalPath $file.Name) -Force
        $global:LogOutput += [PSCustomObject]@{
            Timestamp = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
            Action = "Moved to final folder"
            OriginalName = $file.Name
            NewName = $file.Name
            OriginalFilePath = $file.DirectoryName
            FinalFilePath = $finalPath
            FileSize = Get-ReadableFileSize $file.Length
            RenameType = "N/A"
        }
        $count++
        $progress.ProgressBar.Value = $count
        [System.Windows.Forms.Application]::DoEvents()
    }
    Start-Sleep -Milliseconds 500
    $progress.Form.Close()
    
    # Save CSV log
    $logCsvPath = Join-Path $finalPath ($global:logPrefix + "_LOG.csv")
    $global:LogOutput |
      Select-Object Timestamp, Action, OriginalName, NewName,
                    OriginalFilePath, FinalFilePath,
                    FileSize, RenameType |
      Export-Csv -Path $logCsvPath -NoTypeInformation -Encoding UTF8
    Write-Host "CSV log saved to $logCsvPath"
    
    # Summary
    $renamedCount = ($global:LogOutput | Where-Object { $_.Action -eq "Renamed" -and $_.RenameType -eq "Metadata" }).Count
    $randomCount  = ($global:LogOutput | Where-Object { $_.Action -eq "Renamed" -and $_.RenameType -eq "Random" }).Count
    $movedCount   = ($global:LogOutput | Where-Object { $_.Action -eq "Moved to final folder" }).Count
    
    Write-Host ""
    Write-Host "========== SUMMARY =========="
    Write-Host "Files renamed using metadata : $renamedCount"
    Write-Host "Files renamed with random ID : $randomCount"
    Write-Host "Files moved to final folder  : $movedCount"
    Write-Host "CSV log file saved at: $logCsvPath"
    