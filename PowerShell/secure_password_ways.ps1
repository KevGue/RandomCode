$password = "Password123!@#"
$secureStringPwd = $password | ConvertTo-SecureString -AsPlainText -Force
$secureStringText = $secureStringPwd | ConvertFrom-SecureString
Set-Content "C:\temp\ExportedPassword.txt" $secureStringText
$pwdTxt = Get-Content "C:\temp\ExportedPassword.txt"
$securePwd = $pwdTxt | ConvertTo-SecureString 

$Creds = Get-Credential
$Creds = Export-CliXml -Path 'C:\temp\creds.xml'
$Creds = Import-CliXml -Path 'C:\temp\creds.xml'
$Creds.Password