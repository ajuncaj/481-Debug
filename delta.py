import os
import sys

# Initializes list to [0,n-1]
def init():
	n = int(sys.argv[1])
	listIn = list()	
	for i in range(n):
		listIn.append(i)
	return listIn

# split a list in half
def split_list(list_in):
	half = len(list_in) // 2
	return list_in[:half], list_in[half:]

# Main driver for delta debugger algorthim
def dd(P, C):
	# Base Case
	if (len(C) == 1):
		return C[0]

	#Split C, turn it into strings, craft input strings
	P1, P2 = split_list(C)
	P1str = ' '.join(str(i) for i in P1)
	P2str = ' '.join(str(i) for i in P2)
	Pstr = ' '.join(str(i) for i in P)
	
	in1 = command + ' ' + Pstr + ' ' + P1str
	in2 = command + ' ' + Pstr + ' ' + P2str
	
	# Div+Conc,
	# Send P U P1 and P U P2 to command, recurse if true
	if (os.system(in1)):
		return dd(P, P1)
	if (os.system(in2)):
		return dd(P, P2)
	return list((dd(P + P2, P1), dd(P + P1, P2)))


# sys.argv[1] = size of set n
# sys.argv[2] = command for "interesting"
def main():
	C = init()
	P = list()
	global command
	
	command = sys.argv[2]
	
	x = dd(P, C)
	print(str(x))

if __name__ == '__main__': main()

