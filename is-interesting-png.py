#!/usr/bin/env python

import sys
import os

# Use:python3 is-interesting-png.py 0 1 2 ... n
def main():
	# Coverage of the complete test suite (37.64)
	global fullcoverage
	fullcoverage = 37.64
	
	# Create command in the form of ./pngtest large-png-suite/n.png
	# where n = argv[i]
	# Add png to pngtest
	cmd = "./pngtest large-png-suite/"
	png = ".png > trash.txt"
	for i in range(2, len(sys.argv)):
		command = cmd + str(sys.argv[i]) + png
		os.system(command)

	# Run gcov and redirect to juncajout.txt
	os.system("gcov *.c > juncajout.txt")
	#Yoinked from: 
        #https://stackoverflow.com/questions/46258499/how-to-read-the-last-line-of-a-file-in-python
	# Reads last line of gcov output into last_line. Total line coverage starts @ 15
	with open('juncajout.txt') as f:
		for line in f:
			pass
		last_line = line
		
		# Clean up, check, return
		os.system("rm *.gcda pngout.png juncajout.txt trash.txt")
		print(float(last_line[15:20]))	
		if (float(last_line[15:20]) >= fullcoverage):			
			exit(1)
		else:
			exit(0)
if __name__ == '__main__': main()
