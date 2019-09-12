#VARIABLES
#EDIT THESE THREE
#Only these folders will be copied
$folderstocopy = @('Documents', 'Downloads', 'Pictures')
#Where to create the new folders and copy the files
$destinationfolder = "C:\temp\powershell\destination"
#Where the folders to copy lie
$basefolder = "C:\temp\powershell\users"

#All the folders in the following path will be looked at
$sourcefolders = Get-ChildItem -Path $basefolder

#Each user folder is processed individually
foreach ($baseuserfolder in $sourcefolders) {

    #ACLs of the original folder is being copied into a variable
    $acl = Get-Acl -Path $baseuserfolder.FullName
    #The user folders are being created at the destination
    New-Item -ItemType Directory -Path $destinationfolder\$($baseuserfolder.Name)
    #The copied ACL is applied to the newly created folder
    Set-Acl -Path $destinationfolder\$($baseuserfolder.Name) -AclObject $acl

    #Every folder in the user folder is gotten
    $userfolders = Get-ChildItem -Path $baseuserfolder.FullName

    #Every folder is being processed, becaused it needs to be checked...
    foreach ($folder in $userfolders) {
        #and if the folder is in the defined array...
        if ($folderstocopy.Contains($folder.Name)) {
            #it is being copied recursively
            #ACLs are being inherited automatically from the parent
            Copy-Item -Path $folder.FullName -Destination $destinationfolder\$($folder.Parent.Name) -Recurse -Verbose

        }#if folder is in array
    }#foreach folder in the user's folder
}#foreach user folder
