import numpy
import RPi.GPIO as GPIO
import time
import sys
from datetime import datetime
from time import sleep

LED_PIN = 22
INPUT_WIRE =3

def dec_to_binary(n):
        binNum = bin(n)
        binNum = str(binNum[2:])
        bits = binNum.split()
        send = []

        for i in range (0,8-len(binNum)):
                send.append("0")

        for i in bits:
                send.append(i)

	#adds parity bit
	if(n%2==0):
		send.append("0")
	else:
		send.append("1")

        return ''.join(send)

def setup():
	#set up GPIO pin for sending
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(LED_PIN, GPIO.OUT)
	GPIO.output(LED_PIN,False)


	#gpio for receiving
	GPIO.setup(INPUT_WIRE, GPIO.IN)

def main():
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

			testDec.append(255)
			testDec.append(255)
			testDec.append(255)

			#convert all to binary and get parity
			testBin = []

			for x in testDec:
    				testBin.append(dec_to_binary(x))


			for byte in testBin:
				#convert to NEC protocol:
				toSend = []
				for i in byte:
			    		if i=='1':
		        			toSend.append(0.0016)
	    	    			else:
	        				toSend.append(0.0005)

				correctRec = False;
				#send and wait for reply until correct
				while correctRec !=True:
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
					time.sleep(0.005)
					GPIO.output(22,False)
					time.sleep(0.0002)

					#check reply

					timeout = datetime.now()
					# Loop until we read a 0

					reply = True
					value = 1
        				while value and reply:
                				value = GPIO.input(INPUT_WIRE)
						timeTaken = datetime.now()-timeout
						if timeTaken.microseconds>10000:
							reply = False

			       	 	# Grab the start time of the command
			        	startTime = datetime.now()

					#time the pulse
					while value !=1 and reply:
						value=GPIO.input(INPUT_WIRE)
						timeTaken = datetime.now()-startTime
                                       	 	if timeTaken.microseconds>10000:
                                               		reply = False

					if reply==True:
						parityLen = datetime.now()-startTime
						#print(parityLen.microseconds)
						if parityLen.microseconds<2500:
							correctRec=True
						else:
							print("it told me to resend");
							time.sleep(0.0001)
					else:
						print("resend due to no reply")




if __name__ == "__main__":
    setup()
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
    GPIO.cleanup()




