import re
import time

startTime = time.time()

list1 = ['asdasdasdasd','asdasdasd','2131','asdfgcvb','fgh345df','"VAC_BAN"']
string = ','.join(list1)

if re.search('\\bVAC_BAN\\b', string):
	print('yoyo')

print('It took {0:0.1f} seconds'.format(time.time() - startTime))