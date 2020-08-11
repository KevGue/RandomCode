$devicename = "<DEVICE>"
$port = "<PORT>"
$sendto = "<MAIL>"
$sendfrom = "<MAIL>"
$subject = "<SUBJECT>"
$body = "<BODY>"
$server = "<SERVERIP>"

$connection = Test-NetConnection -computername $devicename -port $port

if ($connection.PingSucceeded -eq "True") {
    Send-MailMessage -to $sendto -Subject $subject -Body $body -From $sendfrom -SmtpServer $server = "<SERVERIP>"
    if ($connection.TcpTestSucceeded -eq "True") {
        Send-MailMessage -to $sendto -Subject $subject -Body $body -From $sendfrom -SmtpServer $server = "<SERVERIP>"
    }
}
