$encrypted = Get-Content <PATH_TO_SECURE_PASSWORD> | ConvertTo-SecureString
$credential = New-Object System.Management.Automation.PsCredential("<ACCOUNTNAME>", $encrypted)
New-PSDrive -name "S" -PSProvider FileSystem -Root <NETWORKSHARE> -Persist -Credential $credential
Copy-Item <SOURCE_DIR> <DEST_DIR> -Recurse
Remove-PSDrive -name "S" -Force
