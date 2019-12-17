import-module remotedesktopservices
$sessions = Get-RDUserSession | Where-Object {$_.username -ne "administrator"}
foreach ($session in $sessions) {
    
    invoke-rduserlogoff -hostserver <SERVER> -UnifiedSessionID $session.unifiedsessionid -Force
}