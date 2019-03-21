###### Henry M - 21/03/2019

import os
import glob
import tkinter
from tkinter import filedialog
from pathlib import Path
import sys

print('\nThis tool will list out lines that txt file(s) in FIRST directory is missing compared to txt file(s) in SECOND directory.')
input('\nPress ENTER to continue....')

root = tkinter.Tk()
root.withdraw()

############################### Directory 1 ###############################
print('\nSelecting first directory...')
dirname1 = filedialog.askdirectory(parent=root, initialdir="/", title='Please select the FIRST directory')
if dirname1 == "":
	print('\nExiting program...')
	sys.exit()

dirname1 = Path(dirname1) # convert path to os' format
txt_files_first = glob.glob(os.path.join(dirname1,'*.txt'))
while not txt_files_first:
	print('Cannot find any txt file in this directory. Please try again...')
	dirname1 = Path(filedialog.askdirectory(parent=root, initialdir="/", title='Please select the FIRST directory'))
	txt_files_first = glob.glob(os.path.join(dirname1,'*.txt'))

print('Directory 1: ' + str(dirname1))

############################### Directory 2 ###############################
print('\nSelecting second directory...')
dirname2 = filedialog.askdirectory(parent=root, initialdir="/", title='Please select the SECOND directory')
if dirname2 == "":
	print('\nExiting program...')
	sys.exit()

dirname2 = Path(dirname2) # convert path to os' format
txt_files_second = glob.glob(os.path.join(dirname2,'*.txt'))
while not txt_files_first:
	print('Cannot find any txt file in this directory. Please try again...')
	dirname2 = Path(filedialog.askdirectory(parent=root, initialdir="/", title='Please select the FIRST directory'))
	txt_files_second = glob.glob(os.path.join(dirname2,'*.txt'))

print('Directory 2: ' + str(dirname2))

############################### Comparison ###############################
i = 1
for file1 in txt_files_first:
	for file2 in txt_files_second:
		print('\nComparing pair ' + str(i) + '...')
		with open(file1, encoding = 'utf-16 le') as f_a, open(file2, encoding = 'utf-16 le') as f_b:
		    a_lines = set(f_a.read().splitlines())
		    b_lines = set(f_b.read().splitlines())
		subdirectory = 'comparison_result'
		try:
			os.mkdir(subdirectory)
		except Exception:
			pass
		result = open(os.path.join(subdirectory, 'result' + str(i) + '.txt'), 'w', encoding = 'utf-16 le')
		result.write('Result of ' + file1 + ' compared to ' + file2 + '\n')
		result.write('=========================================================================================================\n\n')
		for line in b_lines:
			if line not in a_lines:
				result.write(line + '\n')
		result.close()
		print('--------> Done.')
		i+=1
		
input('\nAll comparison has been saved in comparison_result folder (same directory as this tool in).\nPres ENTER in console window to exit...')