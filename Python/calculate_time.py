import pdftotext
import re
import os

timeArray = []
serviceArray = []

calcTime = 0.0
notCalcTime  = 0.0
counter = 0

dotregex = re.compile(r'\,')
os.chdir('/home/pi/Documents/pdf/')

for folder, subfolder, files in os.walk(os.getcwd()):
	for file in files:
		if file.endswith('.PDF') or file.endswith ('.pdf'):
			with open(file,'rb') as f:
				pdf = pdftotext.PDF(f)
				pdfText = ''.join(pdf)

				match = []

				match = re.findall('\d+,\d+.*',pdfText)
				time = re.findall('\d+,\d+',match[0])
				service = re.findall('(IT-Dienst|nicht\sverr|ServicePack).*',match[0])

				time = dotregex.sub('.',time[0])
				time = float(time)

				service = str(service[0])

				timeArray.append(time)
				serviceArray.append(service)

while counter < len(timeArray):
	if serviceArray[counter].startswith('IT'):
		calcTime += timeArray[counter]
	elif serviceArray[counter].startswith('nicht'):
		notCalcTime += timeArray[counter]
	counter += 1

print('Calc time =', calcTime)
print('Non calc time =', notCalcTime)
