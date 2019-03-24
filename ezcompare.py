#Henry M - 21/03/2019

import base64
import os
import sys
import glob
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

class ezcompare(tk.Tk):

	def __init__(self):
		tk.Tk.__init__(self)
		self.title("EzCompare")
		self.geometry("650x300")
		self.resizable(False, False)
		self.iconbitmap('ezcompare_icon.ico')
		self.initComponent()

		# signal to break background thread's loop
		self.do_stop = False

		# override tkinter close button
		self.protocol("WM_DELETE_WINDOW", lambda: self.on_exit())

	# break all loop in background thread, prevent thread from running in background when application already closed
	def on_exit(self): 
		if messagebox.askyesno("Exit", "Do you want to quit the application?"):
			self.do_stop = True
			self.destroy()
	
	def initComponent(self):
		#---------------------------d
		# Main frames
		#---------------------------
		self.topFrame = tk.Frame(self)
		self.topFrame.pack(side=tk.TOP, pady=(20,5))

		self.midFrame = tk.Frame(self)
		self.midFrame.pack(pady=(20,5))

		self.bottomFrame = tk.Frame(self)
		self.bottomFrame.pack(pady=(10,5))

		#---------------------------
		# Directory 1
		#---------------------------
		self.dir1Label = tk.Label(self.topFrame, text = 'Directory 1: ', font = ('Verdana',11))
		self.dir1Label.grid(row = 0, column = 0, padx = (0,1))

		self.dir1PathEntry = tk.Entry(self.topFrame, width = 40, font = ('Verdana',11))
		self.dir1PathEntry.config(state='disable')
		self.dir1PathEntry.grid(row = 0, column = 1, padx = (0,10), pady = (2,0))

		self.selectDirButton1 = tk.Button(self.topFrame, text = "...", width = 2, command = lambda: self.ask_for_directory(self.dir1PathEntry))
		self.selectDirButton1.grid(row = 0, column = 2, padx = (0,20), pady=(0,1))

		#---------------------------
		# Directory 2
		#---------------------------
		self.dir2Label = tk.Label(self.topFrame, text = 'Directory 2: ', font = ('Verdana',11))
		self.dir2Label.grid(row = 1, column = 0, pady = (20,0))

		self.dir2PathEntry = tk.Entry(self.topFrame, width = 40, font = ('Verdana',11))
		self.dir2PathEntry.config(state='disable')
		self.dir2PathEntry.grid(row = 1, column = 1, padx = (0,10), pady = (22,0))

		self.selectDirButton2 = tk.Button(self.topFrame, text = "...", width = 2, command = lambda: self.ask_for_directory(self.dir2PathEntry))
		self.selectDirButton2.grid(row = 1, column = 2, padx = (0,20), pady = (20,1))

		#---------------------------
		# Radio option
		#---------------------------
		self.optionChoice = tk.IntVar()
		self.optionChoice.set(1)

		self.optionLabel = tk.Label(self.midFrame, text = 'Output missing lines of text file(s) in:', font = ('Verdana',10))
		self.optionLabel.grid(row = 0, column = 0)

		self.option1 = tk.Radiobutton(self.midFrame, text = 'First directory', font = ('Verdana',10), variable = self.optionChoice, value = 1)
		self.option1.grid(row = 0, column = 1, pady = (2,0))

		self.option2 = tk.Radiobutton(self.midFrame, text = 'Second directory', font = ('Verdana',10), variable = self.optionChoice, value = 2)
		self.option2.grid(row = 0, column = 2, pady = (2,0))

		#---------------------------
		# Encoding type option
		#---------------------------	
		types = ['', 'utf8', 'utf-16', 'utf-16 be', 'utf-16 le', 'utf-32', 'utf-32 be', 'utf-32 le']
		self.encodingType = tk.StringVar()
		self.encodingType.set(types[4])

		self.encodingLabel = tk.Label(self.midFrame, text = 'Select encoding type:', font = ('Verdana',10))
		self.encodingLabel.grid(row = 1, column = 0, padx = (100,0))

		self.encodingOption = tk.OptionMenu(self.midFrame, self.encodingType, *types)
		self.encodingOption.config(width = 8)
		self.encodingOption.grid(row = 1, column = 1, padx = (0,30))

		#---------------------------
		# Warning/Result message
		#---------------------------
		self.messageText = tk.StringVar()
		self.messageEntry = tk.Label(self.bottomFrame, textvariable = self.messageText , font = ('Verdana',10))
		self.messageEntry.pack()
		
		#---------------------------
		# Compare button
		#---------------------------
		self.compareButton = tk.Button(self.bottomFrame, height = 2, width = 10, text = "COMPARE", command = lambda: self.compare_button_click())
		self.compareButton.pack(pady = (10,0))
		
	def ask_for_directory(self, entry: tk.Entry):
		dirname = filedialog.askdirectory(parent = self, initialdir="/", title='Please select the directory')
		entry.config(state = 'normal')
		entry.delete(0, tk.END)
		entry.insert(0, dirname)
		entry.config(state = 'disable')

	def check_directory(self, dirPathEntry: tk.Entry):
		if dirPathEntry.get() == '':
			self.messageEntry.config(fg = 'red')
			self.messageText.set('Please choose desired directories...')
		else:
			# convert path to corresponding OS' format
			dirname = Path(dirPathEntry.get()) 
			txt_files = glob.glob(os.path.join(dirname,'*.txt'))
			if not txt_files:
				self.messageEntry.config(fg = 'red')
				self.messageText.set('Cannot find any txt file in ' + dirPathEntry.get())
			else:
				return True, txt_files

	def compare_files(self):
		success = True
		noEncode = False

		check1, txt_files_first = self.check_directory(self.dir1PathEntry)
		check2, txt_files_second = self.check_directory(self.dir2PathEntry)

		if check1 and check2:
			i = 1
			for file1 in txt_files_first:
				if self.do_stop:
					break
				for file2 in txt_files_second:
					if self.do_stop:
						break
					if self.encodingType.get() == '':
						f_a = open(file1)
						f_b = open(file2)
					else:
						f_a = open(file1, encoding = self.encodingType.get())
						f_b = open(file2, encoding = self.encodingType.get())
						try:
						    a_lines = list(f_a.read().splitlines())
						    b_lines = list(f_b.read().splitlines())
						    subdirectory = 'comparison_result'
						    try:
						    	os.mkdir(subdirectory)
						    except Exception:
						    	pass

						    result = open(os.path.join(subdirectory, 'result' + str(i) + '.txt'), 'w', encoding = self.encodingType.get())
						    self.messageEntry.config(fg = 'green')
						    self.messageText.set('Comparing pair ' + str(i) + '...')

						    if self.optionChoice.get() == 1:
						    	result.write('Result of ' + file1 + ' compared to ' + file2 + '\n')
						    	result.write('================================================================================\n\n')

						    	for line in b_lines:
						    		isMissing = True

						    		for line1 in a_lines:
						    			try:
						    				if line.split('"')[1].lower() == line1.split('"')[1].lower():
						    					isMissing = False
						    			except:
						    				continue

						    		if isMissing:
						    			print(line)
						    			result.write(line + '\n')
						    			
						    else:
						    	result.write('Result of ' + file2 + ' compared to ' + file1 + '\n')
						    	result.write('================================================================================\n\n')

						    	for line in a_lines:
						    		isMissing = True

						    		for line1 in b_lines:
						    			try:
						    				if line.split('"')[1].lower() == line1.split('"')[1].lower():
						    					isMissing = False
						    			except:
						    				continue

						    		if isMissing:
						    			print(line)
						    			result.write(line + '\n')
						    			
						    result.close()
						    f_a.close()
						    f_b.close()
						    i+=1
						except Exception as e:
							print(str(e))
							success = False
							self.messageEntry.config(fg = 'red')
							self.messageText.set('Incorrect encoding type.')
			if success:
				self.messageEntry.config(fg = 'green')
				self.messageText.set('Result has been saved in comparison_result folder (same directory with this tool).')

	def compare_button_click(self):
		self.compare_files_thread = threading.Thread(target = self.compare_files)
		self.compare_files_thread.start()

app = ezcompare()
app.mainloop()
