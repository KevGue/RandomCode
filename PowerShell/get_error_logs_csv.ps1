#Only a few logs are checked
$relevantlogs = @('Application','System', 'Security')

#The timeframe to check
$enddate = (Get-Date).Date
$startdate = (Get-Date).AddDays(-7).Date

#Loop through each log and...
foreach ($log in $relevantlogs) {
    #Check the events
    Get-WinEvent -LogName $log | Where-Object {($_.timecreated.date -le $enddate -and $_.timecreated.date -ge $startdate) -and `
         ($_.leveldisplayname -eq "Error" -or $_.leveldisplayname -eq "Fehler")} | Export-Csv -Path C:\temp\powershell\logs.csv

}
