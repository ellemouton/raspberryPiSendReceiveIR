import sys
toWrite ="["

for j in range(0,3):
	for i in range (0,255):
		if i<254:
			toWrite+=str(i)+","
		else:
			toWrite+=str(i)
	if j<2:
		toWrite+=","


toWrite+="]"
f = open('compareBits.txt','w')
f.write(toWrite)
f.close()
