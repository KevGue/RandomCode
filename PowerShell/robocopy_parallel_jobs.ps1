$folders = Get-ChildItem -Path <SOURCE_PATH> -Directory

foreach ($folder in $folders) {
    $src = $folder.FullName
    $dest = "<DEST_PATH>"
    $log = "C:\temp\robocopy_$folder-$(Get-Date -Format "yyyy_MM_dd_HH_mm").txt"
    $log
    $scriptblock = {
        param($src,$dest,$log)
        robocopy $src $dest /E /ZB /R:3 /W:1 /MT:32 /V /XC /XN /XO | Out-File $log

    }
    Start-Job -ScriptBlock $scriptblock -Name $folder.Name -ArgumentList $src,$dest,$log
}