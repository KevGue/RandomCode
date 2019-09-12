import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog as fd
import re
import sys
import os
from threading import Thread
from tqdm import tqdm
import pyperclip
import time

stopper = False

#Class that is necessary to print stderr and stdout to a text widget
class PrintToText(object):
	def write(self,s):
		scrolEOF.insert(tk.END,s)

#the main function for the parsing
def logParser(logToParse, searchType, interface, IPToParse, PortToParse, RegexParse, resultingFile):
	start_time = time.time()
	
	#Clear the text fields
	scrol.delete(1.0, tk.END)
	scrolEOF.delete(1.0,tk.END)
	
	#Check if log has been selected
	if logToParse == '':
		scrol.insert(tk.INSERT,'Please specify a file\n')
		getFileName()

	#Assign variables for regex
	if interface == 0:
		interface = 'intern'
	elif interface == 1:
		interface = 'partner'
	elif interface == 2:
		interface = 'dmz'
	elif interface == 3:
		interface = 'WAN'
	elif interface == 4:
		interface = 'gast-netz'
	elif interface == 5:
		interface = '(WAN|dmz|intern|partner|management|gast-netz)?'
	
	if IPToParse == '':
		IPToParse = '.*'

	if PortToParse == '':
		PortToParse = '.*'
	
	#Variables are set
	match = []
	fileIsOpen = 0
	sys.stdout = PrintToText()
	sys.stderr = PrintToText()
	counter = 0
	matchCounter = 0 #Counter for all the matches
	
	#Due to weirdness with re.compile the regex has to be set now for use with re.findall later
	IPToParse = IPToParse.replace('.','\.').replace('.*','..*')
	
	#This if needs to be here otherwise it creates problems with the regex later
	if IPToParse == '\..*':
		IPToParse = '.*'
	
	#Multiple files can be selected
	for log in logToParse:
		log = log.replace('{','').replace('}','')
	
		with open(log) as infile:#The file is opened
			scrol.insert(tk.INSERT,'\n' + log + '\n') #The filename is written so results can be connected with files
			if resultingFile != '': #Check if a results file has to be created
				if os.path.isfile(resultingFile):
					os.remove(resultingFile)
				fileForResults = open(resultingFile, 'a+')
				fileIsOpen = 1
			for line in tqdm(infile, file=sys.stdout): #And read line by line, because the logs can be over 500MB
				if stopper:
					return
			
				#This part is used to reset the text widget since it is being filled via the file=sys.stdout (scrolEOF is the redirect from the class PrintToText)
				#This is not necessary, it's simply there to show something is being done
				counter += 1 
				if counter == 2000:
					scrolEOF.delete(1.0,tk.END)
					counter = 0
					
				if searchType == 0: #Check the argument for the type and use the correct regex
					#match = re.findall('((.*' + ' for ' + interface + ':' + IPToParse  + '/' + PortToParse + ').*)',line)
					match = re.findall('((\w{3} \d{1,2} \d\d:\d\d:\d\d firewall %ASA-\d-\d{1,6}: \w+ \w+ (\(no connection\))?(\w+)?( connection)? (for |from)?(\d+)?( for )?(faddr)?( )?' + interface + '(:)?' + IPToParse + '/' + PortToParse + ').*)',line)

				elif searchType == 1:
					match = re.findall('((.* to ' + interface + ':' + IPToParse + '/' + PortToParse + ' .*))',line)
					#match = re.findall('((\w{3} \d{1,2} \d\d:\d\d:\d\d firewall %ASA-\d-\d{1,6}: \w+ \w+ (\(no connection\))?(\w+)?( connection)? (for |from)?(\d+)?( for )?(faddr)?( )?((WAN|dmz|intern|partner|management|gast-netz)[A-Za-z]?:)?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,5}) (\((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\/\d{1,5})\))?( )?to ' + interface + ':' + IPToParse + '/' + PortToParse + ' .*))',line)
					
				elif searchType == 2:
					#match = re.findall('((.*' + IPToParse + '/' + PortToParse + ').*)',line)
					match = re.findall('((\w{3} \d{1,2} \d\d:\d\d:\d\d firewall %ASA-\d-\d{1,6}: \w+ \w+ (\(no connection\))?(\w+)?( connection)? (for |from)?(\d+)?( for )?(faddr)?( )?(\w+[A-Za-z]:)?.*' + IPToParse + '/' + PortToParse + ').*)',line)
				
				elif searchType == 3:
					#match = re.findall('((.*' + IPToParse + '/' + PortToParse + ').*)',line)
					match = re.findall('((.*' + RegexParse + '.*))',line)
					
				
				if match != []: #Only the matches with actual content are printed
					scrol.insert(tk.INSERT,match[0][0]+'\n')
					if fileIsOpen: #Write the results to the results file
						fileForResults.write(match[0][0]+'\n')
					matchCounter += 1
			
			elapsed_time = time.time() - start_time
			elapsed_time = round(elapsed_time, 2)
			
			#The scrolEOF field is being filled with results info
			scrolEOF.delete(1.0,tk.END)
			scrolEOF.insert(tk.INSERT,'Elapsed Time for parse: ' + str(elapsed_time) + 's\n')
			scrolEOF.insert(tk.INSERT,'Matches in file:' + str(matchCounter) + '\n')
			scrolEOF.insert(tk.INSERT,'EOF reached')
			
			#The results file is being closed
			if fileIsOpen:
				fileForResults.close()

#Function that starts the log parsing in a thread upon pressing the Parse log(s) button
def click_me():
	run_thread = Thread(target=logParser, args=(logFile.get().split(' '),SearchRadioVar.get(),IntRadioVar.get(),IPAddress.get(), port.get(), regex.get(), resultsFile.get()))
	run_thread.start()

#Function that copies the matches to the clipboard upon pressing the "Copy results to clipboard" button
def copyOutput():
	output = scrol.get("1.0",tk.END)
	pyperclip.copy(output)

def stopParse():
	global stopper
	stopper = True

#Function that lets user select the files upon pressing the "Browse logfile(s)" button and displays them in a field
def getFileName():
	fileList = []
	fName = fd.askopenfilename(parent=win,multiple = 1)
	if len(logFileEntry.get()) > 0:
		logFileEntry.delete(0,tk.END)
	for selFile in fName:
		fileList.append(selFile.replace('/','\\'))
	logFileEntry.insert(0,fileList)

#Function that lets user select a results file upong pressing the "Save results to" button and displays it in a field
def resFileName():
	rName = fd.asksaveasfilename(parent=win, filetypes = (("text files","*.txt"),("all files","*.*")))
	if len(resultsFileEntry.get()) > 0:
		resultsFileEntry.delete(0,tk.END)
	resultsFileEntry.insert(0,rName.replace('/','\\'))

#The tkinter window is being created
win = tk.Tk()
win.state('zoomed')

win.title('Cisco ASA Logparser v4')
inWin = ttk.LabelFrame(win, text = 'Logparser')
inWin.grid(column=0, row=0, padx=8, pady=10)

fileMgr = ttk.LabelFrame(inWin, text = 'File management')
fileMgr.grid(column=0, row=0, padx=8, pady=10, sticky=tk.W)

#Browse logfile button
logFileBrowse = ttk.Button(fileMgr, text='Browse logfile(s)... ', command=getFileName)
logFileBrowse.grid(column=0, row=0, sticky=tk.W)

#Display path to logfile
logFile = tk.StringVar()
entryLen = 88
logFileEntry = ttk.Entry(fileMgr,width=entryLen, textvariable=logFile)
logFileEntry.grid(column=1, row=0, padx=5, sticky=tk.W)

#Browse save to button
saveToFileBrowse = ttk.Button(fileMgr, text='Save results to... (optional)', command=resFileName)
saveToFileBrowse.grid(column=0, row=2, sticky=tk.W)

#Display path to results file
resultsFile = tk.StringVar()
resultsFileEntry = ttk.Entry(fileMgr,width=entryLen, textvariable=resultsFile)
resultsFileEntry.grid(column=1, row=2, padx=5, sticky=tk.W)

searchPar = ttk.LabelFrame(inWin, text = 'Search parameters')
searchPar.grid(column=0, row=1, padx=8, pady=2, sticky=tk.W)

#Create radiobuttons for type of search
SearchRadioPicks = ['Search in source', 'Search in destination', 'Search all', 'Regex search']
SearchRadioVar = tk.IntVar()
for col in range(4):	
	curRad = tk.Radiobutton(searchPar, text=SearchRadioPicks[col], variable=SearchRadioVar, 
	value=col)
	curRad.grid(column=col, row=1, sticky=tk.W)

#Create radiobuttons for type of interface
IntRadioPicks = ['intern', 'partner', 'dmz', 'WAN', 'gast-netz', 'all interfaces']
IntRadioVar = tk.IntVar()
for col in range(6):
	curRad = tk.Radiobutton(searchPar, text=IntRadioPicks[col], variable=IntRadioVar, 
	value=col)
	curRad.grid(column=col, row=3, sticky=tk.W)

#Create label and entry field for IP
IPLabel = ttk.Label(searchPar, text='IP Address:')
IPLabel.grid(column=0, row=4, padx=5, sticky=tk.W)

IPAddress = tk.StringVar()
entryLen = 15
IPAddressEntry = ttk.Entry(searchPar,width=entryLen, textvariable=IPAddress)
IPAddressEntry.grid(column=1, row=4, padx=5, pady=5, sticky=tk.W)

#Create label and entry field for port
PortLabel = ttk.Label(searchPar, text='Port:')
PortLabel.grid(column=0, row=5, padx=5, sticky=tk.W)

port = tk.StringVar()
entryLen = 15
PortEntry = ttk.Entry(searchPar,width=entryLen, textvariable=port)
PortEntry.grid(column=1, row=5, padx=5, sticky=tk.W)

#Create label and entry field for Regex
RegexLabel = ttk.Label(searchPar, text='Regex:')
RegexLabel.grid(column=0, row=6, padx=5, sticky=tk.W)

regex = tk.StringVar()
entryLen = 15
RegexEntry = ttk.Entry(searchPar,width=entryLen, textvariable=regex)
RegexEntry.grid(column=1, row=6, padx=5, pady=5, sticky=tk.W)

#Output window
scrol_w = 234
scrol_h = 43
scrol = scrolledtext.ScrolledText(inWin, width=scrol_w, height=scrol_h, wrap=tk.WORD)
scrol.grid(column=0, row=5, columnspan=3, sticky=tk.W)
scrol.configure(state='normal')

#Output window EOF
scrol_w = 30
scrol_h = 3
scrolEOF = scrolledtext.ScrolledText(inWin, width=scrol_w, height=scrol_h, wrap=tk.WORD)
scrolEOF.grid(column=1, row=1, columnspan=3, padx=600, sticky=tk.W)

printInputs = ttk.Button(inWin, text='Parse log(s)', command=click_me)
printInputs.grid(column=0, row=2, padx=8, pady=8, sticky=tk.W)

copyOutput = ttk.Button(inWin, text='Copy results to clipboard', command=copyOutput)
copyOutput.grid(column=0, row=2, padx=190, sticky=tk.W)

stopParsing = ttk.Button(inWin, text='Stop parsing', command=stopParse)
stopParsing.grid(column=0, row=2, padx=100, sticky=tk.W)

IPAddressHelperText = '''Wildcard usage for IP:
192.168.0.1 - matches that exact IP
192.168.0.* - matches the entire network ranging from 192.168.0.0 to 192.168.0.255
192.168.*.1 - matches everything from 192.168.0.1 to 192.168.255.1
'''

helpLabel = ttk.Label(inWin,text=IPAddressHelperText)
helpLabel.grid(column=1, row=1, sticky=tk.W)


win.mainloop()
