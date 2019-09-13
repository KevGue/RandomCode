$excluded = @('PSChildName','PSDrive','PSParentPath','PSPath','PSProvider')

#All the shares are being gotten, except some PowerShell stuff, because it's not that easy
$sharenames = Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Shares" | Get-Member | Where-Object {$_.membertype -eq "NoteProperty" -and $excluded -notcontains $_.name} | Select-Object -Property Name

#Loop through every share
foreach ($sharename in $sharenames) {

	#Old and worked with array that contains the names of shares
    #$share = Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Shares" -name $sharename
    #$newregvalue = $share.$sharename -replace  "<SEARCH>", "<REPLACE>"
	#Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Shares" -Name $sharename -Value $newregvalue

    #New, but untested
    #Get each share's properties
    $share = Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Shares" -Name $sharename.Name | Select-Object -ExpandProperty $sharename.Name
    #Assemble the new value
    $newregvalue = $share -replace "<SEARCH>", "<REPLACE>"
    #Write the new value
    Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Shares" -Name $sharename.Name -Value $newregvalue
}