import PyPDF2, os
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(multiple = 1)

os.chdir(os.path.dirname(file_path[0]))

waterMarkFile = open('C:\Path\To\.pdf', 'rb')
pdfWatermarkReader = PyPDF2.PdfFileReader(waterMarkFile)

for selectedFile in file_path:

        rechnungFile = open(selectedFile, 'rb')
        pdfReader = PyPDF2.PdfFileReader(rechnungFile)

        rechnungFirstPage = pdfReader.getPage(0)
        rechnungFirstPage.mergePage(pdfWatermarkReader.getPage(0))

        pdfWriter = PyPDF2.PdfFileWriter()
        pdfWriter.addPage(rechnungFirstPage)

        for pageNum in range(1, pdfReader.numPages):
            pageObj = pdfReader.getPage(pageNum)
            pdfWriter.addPage(pageObj)

        newFileName = os.path.basename(os.path.splitext(selectedFile)[0]) + '_gebucht' + '.pdf'
        resultPdfFile = open(newFileName, 'wb')
        pdfWriter.write(resultPdfFile)
        rechnungFile.close()
        resultPdfFile.close()

waterMarkFile.close()
