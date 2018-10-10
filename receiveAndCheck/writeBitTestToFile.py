import sys
toWrite ="["

for j in range(0,5):
	for i in range (0,255):
		if i<254:
			toWrite+=str(170)+"," #toWrite+=str(i)+","
		else:
			toWrite+=str(170) #toWrite+=str(i)
	if j<4:
		toWrite+=","


toWrite+="]"
f = open('compareBits.txt','w')
#f = open('interface2.txt','w')
f.write(toWrite)
f.close()
