import PyPDF2, re, os

print('Input path to folder:')
searchFolder = input()

print('Input text:')
searchText = input().lower()
searchReg = re.compile(searchText)
somethingFound = []
errorFile = []

for folderName, subfolder, files in os.walk(searchFolder):
    for file in files:
        print('Current file:', file)
        currentFile = os.path.join(folderName, file)
        
        try:
            pdfFileObj = open(currentFile, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    
            for i in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(i)

                text = pageObj.extractText()
                text = text.lower()
                
                match = searchReg.findall(text)
                print(match)
                if match != []:
                    somethingFound.append(currentFile)
        except:
            errorFile.append(currentFile)
            continue
        
print('\nFiles with text:',somethingFound)
print('\nFiles with errors:',errorFile)
