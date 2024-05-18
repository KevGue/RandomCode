'''Remove a specific string from all files in a path'''

import os

path = "C:\\TEST\\PATH"
removeString = "TESTSTRING"

os.chdir(path)

for filename in os.listdir(path):
    newFilename = filename
    if removeString in filename:
        newFilename = filename.replace(removeString,'')

    newFilename = newFilename.lstrip()
    os.rename(filename, newFilename)
