#VARIABLES
$folderToGetACL = 'C:\temp\powershell'
$exportDestinationFileName = 'C:\temp\powershell\acl_ps.csv'

#Get all files and folders
$basefolder = Get-ChildItem -Path $folderToGetACL -Recurse

#Build an array for later
$toExport = @()

#Loop through each folder and get every file
foreach ($file in $basefolder) {

    #Get the ACL entries
    $acl = Get-Acl -Path $file.FullName
    
    #Loop through each ACE in the ACL
    foreach ($entry in $acl.Access) {
        #Build a propertylist
        $entryArray = [ordered]@{'Foldername' = $file.FullName;
                        'User or group' = $entry.IdentityReference;
                        'Rights' = $entry.FileSystemRights;
                        'Type' = $entry.AccessControlType;
                        'Inherited' = $entry.IsInherited}

        #Populate an array with a new object
        $toExport += New-Object -TypeName PSObject -Property $entryArray
        
    }#foreach ACE
}#foreach file

#Export the array to a .CSV
$toExport | Export-Csv -Path $exportDestinationFileName -NoTypeInformation