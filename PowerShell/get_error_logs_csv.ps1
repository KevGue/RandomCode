$relevantlogs = @('Application','System', 'Security')


$enddate = (Get-Date).Date
$startdate = (Get-Date).AddDays(-7).Date

#$lognames = Get-WinEvent -ListLog * | Select-Object LogName

foreach ($log in $relevantlogs) {
    Get-WinEvent -LogName $log | Where-Object {($_.timecreated.date -le $enddate -and $_.timecreated.date -ge $startdate) -and `
         ($_.leveldisplayname -eq "Error" -or $_.leveldisplayname -eq "Fehler")} | Export-Csv -Path C:\temp\powershell\logs.csv

}