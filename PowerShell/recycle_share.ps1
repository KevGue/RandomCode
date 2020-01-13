$encrypted = Get-Content <PATH_TO_SECURE_PASSWORD> | ConvertTo-SecureString
$credential = New-Object System.Management.Automation.PsCredential("<ACCOUNTNAME>", $encrypted)
New-PSDrive -name "S" -PSProvider FileSystem -Root <NETWORKSHARE> -Persist -Credential $credential
Get-ChildItem -Path S:\#recycle | Where-Object {$_.Attributes -eq "Directory, Archive" -or $_.Extension -eq ".bin"} | Remove-Item -Recurse
Remove-PSDrive -name "S" -Force