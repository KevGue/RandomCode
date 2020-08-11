$source = "C:\temp\random"
$destination = "C:\temp\powershell"
$folders = get-childitem -path $source

foreach ($folder in $folders) {
    if ($folder.basename -match "[a-dA-D].*") {
        robocopy $folder.FullName $destination\$folder /E /R:1 /W:1 /V
    }
}