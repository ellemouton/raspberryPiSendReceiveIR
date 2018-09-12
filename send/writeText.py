import sys

if len(sys.argv)>1:
	toWrite = sys.argv[1]
	f = open('interface1.txt','w')
	f.write(toWrite)
	f.close()
