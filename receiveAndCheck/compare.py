preBits = []
postBits = []


file = open('compareBits.txt', 'r+')
content = file.read()
data = (content[1:len(content)-1]).split(",")


for d in data:
	preBits.append(int(d))

file.close()

file = open('interface2.txt', 'r+')
content = file.read()
data = (content[1:len(content)-1]).split(",")


for d in data:
        postBits.append(int(d))

file.close()


print("PRESEND")
print(len(preBits))

print("POSTSEND")
print(len(postBits))

print("NUMBER OF LOST BYTES:")
print(len(preBits)-len(postBits))

errorCounter = 0

if(len(preBits)>len(postBits)):
	for i in range(0, len(postBits)):
		if preBits[i]!=postBits[i]:
			errorCounter+=1
else:
        for i in range(0, len(preBits)):
                if preBits[i]!=postBits[i]:
                        errorCounter+=1


print("NUMBER OF BYTE ERRORS:")
print(errorCounter)
