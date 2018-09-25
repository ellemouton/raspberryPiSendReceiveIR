import numpy
import RPi.GPIO as GPIO
import time
import sys
from datetime import datetime
from time import sleep

LED_PIN = 22
INPUT_WIRE =3

global entireFile
global separate

def dec_to_binary(n):
        binNum = bin(n)
        binNum = str(binNum[2:])
        bits = binNum.split()
        send = []

        for i in range (0,8-len(binNum)):
                send.append("0")

        for i in bits:
                send.append(i)

        return ''.join(send)


def setup():
	#set up GPIO pin for sending
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(LED_PIN, GPIO.OUT)
	GPIO.output(LED_PIN,False)

	#gpio for receiving
	GPIO.setup(INPUT_WIRE, GPIO.IN)


def readFromFile():
	global entireFile

	file = open('interface1.txt', 'r+')
    	content = file.read()

	if len(content)>0:
		data = (content[1:len(content)-1]).split(",")

        	entireFile = []

        	for d in data:
            		entireFile.append(int(d))
		entireFile.append(255)
		entireFile.append(255)
		entireFile.append(255)

            	file.truncate(0)
		file.close()
		return True
	return False

def convertToBinary(dec):
#convert all to binary

	testBin = []

	for x in dec:
		testBin.append(dec_to_binary(x))

	return testBin


def send(toSend):
	#start command
	GPIO.output(22, True)
	time.sleep(0.009)
	GPIO.output(22,False)
	time.sleep(0.0045)

	for i in toSend:
		GPIO.output(22, True)
       		time.sleep(0.0005)
       		GPIO.output(22, False)
       		time.sleep(i)

	#stop command
	GPIO.output(22, True)
	time.sleep(0.1)
	GPIO.output(22,False)
	time.sleep(0.005)

def checkReply():
	# Loop until we read a 0

	print("waiting for reply")
	value = 1
    	while value:
        	value = GPIO.input(INPUT_WIRE)

	# Grab the start time of the command
	startTime = datetime.now()

	#time the pulse
	while value !=1:
		value=GPIO.input(INPUT_WIRE)


	pulseLen = datetime.now()-startTime

	time.sleep(1)
	print(pulseLen.microseconds)
	if pulseLen.microseconds<2500:
		return True
	else:
		return False


def main():
	global entireFile
	global separate

	while True:
		if readFromFile():

			#split array into chuncks of 50 or less
			length = len(entireFile)
			startPos = 0
			limit = 20
			separate = []

			separate.append(entireFile[startPos:limit+startPos])
			startPos+=limit
			length-=limit

			while(length>limit):
				separate.append(entireFile[startPos:limit+startPos])
				startPos +=limit
				length -=limit

			if(startPos<len(entireFile)):
				separate.append(entireFile[startPos:len(entireFile)])



			#for each chunk
			for chunk in separate: #[2,1]
				arr = chunk
				l = len(chunk)
				hashVal = hash(str(arr))%255; #change this
				print(hashVal)
				print(str(arr))

				arr.append(l)
				arr.append(hashVal)

				binChunk = convertToBinary(arr) #["10","01"]
				allTogether = ''.join(binChunk) #1001

				#convert to NEC protocol:
				toSend = []

				for i in range(0, len(allTogether)):

		   			if allTogether[i]=='1':
		        			toSend.append(0.0016)
	    	    			else:
	        				toSend.append(0.0005)


	        		correctReply =  False

	        		while(correctReply==False):
	        			send(toSend)
					print("sending")
	        			correctReply = checkReply()



if __name__ == "__main__":
    setup()
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
    GPIO.cleanup()




