import RPi.GPIO as GPIO
import math
import os
import numpy as np
import sys
import time
from datetime import datetime
from time import sleep

INPUT_WIRE = 4
LED_PIN = 27

global songEndCounter
global song

def setup():
	global songEndCounter
	global song

	#set up pin for receiving
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(INPUT_WIRE, GPIO.IN)

	#set up GPIO pin for sending
	GPIO.setup(LED_PIN, GPIO.OUT)

	songEndCounter = 0
	song = []

def sendToFile():
	global songEndCounter
	global song

	#construct string for text file
	exportString = "["+",".join(song[0:len(song)-3])+"]"
        print(exportString)

        #write to text file
        f = open('interface2.txt','w')
        f.write(exportString)
        f.close()
	song = []
	songEndCounter = 0

def main():
	global songEndCounter
	global song

	while True:
		resend = False
		#check for start command:
		value = 1
		# Loop until we read a 0

		while value:
			value = GPIO.input(INPUT_WIRE)

		# Grab the start time of the command
		startTime = datetime.now()
		timeout=  False
		while value!=1 and timeout == False:
			value = GPIO.input(INPUT_WIRE)

			timeTaken = datetime.now()-startTime
			if timeTaken.microseconds>20000:
				timeout = True


		startUp = datetime.now()-startTime
		startTime = datetime.now()

		while value and timeout == False:
               		value = GPIO.input(INPUT_WIRE)
			timeTaken = datetime.now()-startTime
                        if timeTaken.microseconds>20000:
                                timeout = True


		startDown = datetime.now()-startUp


		#if start command correct, continue. else play back incorrect parity
		if (startUp.microseconds>7000 and timeout==False): # and startDown.microseconds>3000):

			startTime = datetime.now()

			# Used to buffer the command pulses
			command = []

			# Used to keep track of transitions from 1 to 0
			previousVal = 0

			while True:
				if value != previousVal:
					# The value has changed, so calculate the length of this run
					now = datetime.now()
					pulseLength = now - startTime
					startTime = now

					command.append((previousVal, pulseLength.microseconds))

					if pulseLength.microseconds>3000:
						break

				previousVal = value
				value = GPIO.input(INPUT_WIRE)

			#get rid of start and stop commands and decode

			commandCut = ""

			for (val, pulse) in command[0:len(command)-1]:
                		if val == 1:
					if pulse>1000:
						commandCut+="1"
					else:
						commandCut+="0"


			#check if there are 9 bits (byte plus parity)
			if(len(commandCut)==9):
				#convert to dec and check parity
				binaryNum = int("".join(commandCut[0:len(commandCut)-1]),2)
				parity = int(commandCut[len(commandCut)-1])

				#check if num and parity match

				if binaryNum%2==0 and parity==1:
					#mistake
					resend = True
					print("resend due to parity")
				elif binaryNum%2!=0 and parity ==0:
					#mistake
					resend = True
					print("resend due to parity")
				else:
					song.append(str(binaryNum))
					if binaryNum==255:
						songEndCounter+=1

			else:
				resend = True
				print("resend due to not 9")
				print(binaryNum)



		#send signal back:
		if(resend == True):
			GPIO.output(LED_PIN, True)
        		time.sleep(0.004)
        		GPIO.output(LED_PIN,False)

		else:
			GPIO.output(LED_PIN, True)
               		time.sleep(0.001)
               		GPIO.output(LED_PIN,False)
			if songEndCounter==3:
				sendToFile()




if __name__ == "__main__":
    setup()
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
    GPIO.cleanup()
