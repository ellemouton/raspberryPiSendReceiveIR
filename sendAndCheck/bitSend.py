import sys
toWrite ="["
counter=0

for j in range(0,3):
	for i in range (0,255):
		if i<254:
			toWrite+=str(i)+","
			counter+=1
		else:
			toWrite+=str(i)
			counter+=1
	if j<2:
		toWrite+=","

print(counter)
toWrite+="]"
f = open('interface1.txt','w')
f.write(toWrite)
f.close()
