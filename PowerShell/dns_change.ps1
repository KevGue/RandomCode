Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
New-Item -ItemType Directory -Path C:\tmp
Get-DnsClientServerAddress | Out-File C:\tmp\dnsaddress.txt #Save DNS addresses to be safe

$newaddresses = @("10.0.1.4","10.0.1.5") #Array with new server

$netadapter = Get-NetAdapter | Where-Object {($_.MediaType -eq "802.3") -and ($_.status -eq "Up")} #Filter for ethernet adapters that are up

foreach ($adapter in $netadapter) {
    #Only change adapters with IPv4 and DNS addresses
    Get-DnsClientServerAddress -AddressFamily IPv4 -InterfaceIndex $adapter.ifIndex | Where-Object {$_.ServerAddresses -ne {}} | Set-DnsClientServerAddress -ServerAddresses $newaddresses
}