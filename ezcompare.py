###### Henry M - 21/03/2019

import os
import sys
import glob
import tkinter
from tkinter import filedialog
from pathlib import Path


ENCODING_TYPE = 'utf-16 le' # encoding type of comparing text files

def ask_for_directory():
	root = tkinter.Tk()
	root.withdraw()
	dirname = filedialog.askdirectory(parent=root, initialdir="/",title='Please select the directory')

	if dirname == "":
		print('\nExiting program...')
		sys.exit()

	dirname = Path(dirname) # convert path to corresponding OS' format
	txt_files = glob.glob(os.path.join(dirname,'*.txt'))
	while not txt_files: # if no txt file in the directory
		print('Cannot find any txt file in this directory. Please try again...')
		dirname = Path(filedialog.askdirectory(parent=root, initialdir="/", title='Please select the first directory'))
		txt_files = glob.glob(os.path.join(dirname,'*.txt'))

	return dirname, txt_files

print('\nWelcome to ezcompare!')
input('\nPress ENTER to continue....')

##################################################### Directory 1 ###########################################################

print('\nSelecting first directory...')
dirname1, txt_files_first = ask_for_directory()
print('Directory 1: ' + str(dirname1))

##################################################### Directory 2 ###########################################################

print('\nSelecting second directory...')
dirname2, txt_files_second = ask_for_directory()
print('Directory 2: ' + str(dirname2))

######################################################   Menu   #############################################################

i = 1
menu = 0
menu = int(input('\nPlease choose an option.\n'
				 'Output lines that text file(s) in:\n'
				 '  1. First directory are misisng\n'
				 '  2. Second directory are missing\n'
				 '- Your choice... : '))

##################################################### Comparison ############################################################

for file1 in txt_files_first:
	for file2 in txt_files_second:
		with open(file1, encoding = ENCODING_TYPE) as f_a, open(file2, encoding = ENCODING_TYPE) as f_b:
		    a_lines = set(f_a.read().splitlines())
		    b_lines = set(f_b.read().splitlines())
		subdirectory = 'comparison_result'
		try:
			os.mkdir(subdirectory) # create new subdirectory
		except Exception:
			pass # ignore if it is already existed
		result = open(os.path.join(subdirectory, 'result' + str(i) + '.txt'), 'w', encoding = ENCODING_TYPE)
		if menu == 1:
			print('\nComparing pair ' + str(i) + '...')
			result.write('Result of ' + file1 + ' compared to ' + file2 + '\n')
			result.write('================================================================================\n\n')
			for line in b_lines:
				if line not in a_lines:
					result.write(line + '\n')
		elif menu == 2:
			print('\nComparing pair ' + str(i) + '...')
			result.write('Result of ' + file2 + ' compared to ' + file1 + '\n')
			result.write('================================================================================\n\n')
			for line in a_lines:
				if line not in b_lines:
					result.write(line + '\n')
		else:
			print('Invalid choice.')
			sys.exit()
		result.close()
		print('--------> Done.')
		i+=1

#############################################################################################################################

input('\nAll result has been saved in comparison_result folder (same directory with this tool).\nPres ENTER to exit...')