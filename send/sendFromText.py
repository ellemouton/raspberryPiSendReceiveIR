import numpy
import RPi.GPIO as GPIO
import time
import sys


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

#set up GPIO pin
LED_PIN = 22
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

while True:
        file = open('interface1.txt', 'r+')
        content = file.read()

	if len(content)>0:

                data = (content[1:len(content)-1]).split(",")
                testDec= []

                for d in data:
                        testDec.append(int(d))
                file.truncate(0)

		file.close()

		#convert all to binary
		testBin = []
		for x in testDec:
    			testBin.append(dec_to_binary(x))

		#put all in one
		allTogether = ''.join(testBin)

		#convert to NEC protocol:
		toSend = []

		for i in range(0, len(allTogether)):

		    if allTogether[i]=='1':
		        toSend.append(0.0016)
	    	    else:
	        	toSend.append(0.0005)

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
		time.sleep(0.05)
		GPIO.output(22,False)
