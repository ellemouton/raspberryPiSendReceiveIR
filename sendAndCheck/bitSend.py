import sys
toWrite ="["

for j in range(0,5):
	for i in range (0,255):
		if i<254:
			toWrite+=str(170)+","
		else:
			toWrite+=str(170)
	if j<4:
		toWrite+=","


toWrite+="]"
f = open('interface1.txt','w')
f.write(toWrite)
f.close()
