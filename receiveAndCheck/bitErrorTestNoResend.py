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
global resendCount

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
	print("number of resends:")
	print(resendCount)
	#write to text file
	f = open('interface2.txt','w')
	f.write(exportString)
	f.close()
	song = []
	songEndCounter = 0

def resendSignal():

		global resendCount

		resendCount+=1
		time.sleep(0.2) #changed from 0.5
		GPIO.output(LED_PIN, True)
		time.sleep(0.0025)
		GPIO.output(LED_PIN,False)
		time.sleep(0.0045)
		print("resend")

def signalCorrect():
		print("correct") #changed from 0.5
		time.sleep(0.2)
		GPIO.output(LED_PIN, True)
		time.sleep(0.001)
		GPIO.output(LED_PIN,False)
		time.sleep(0.0045)

def main():
	global songEndCounter
	global song
	global resendCount

	resendCount = 0

	while True:
		value = 1
		# Loop until we read a 0

		while value:
			value = GPIO.input(INPUT_WIRE)

		# Grab the start time of the command
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

				if pulseLength.microseconds>20000:
					break

			previousVal = value
			value = GPIO.input(INPUT_WIRE)

		#get rid of start and stop commands and decode

		commandCut = ""

		for (val, pulse) in command[2:len(command)-1]:
			if val == 1:
				if pulse>550:
					commandCut+="1"
				else:
					commandCut+="0"

		#split into groups of 8 (bytes)
		#if(len(commandCut)%8==0):
		bytes = np.array_split(list(commandCut), len(commandCut)/8)

			#construct string for text file
		received = []

		for b in bytes:
			received.append(int("".join(b),2))


		correctLen = received[len(received)-2]
		correcthashVal = int(received[len(received)-1])

		hashVal = hash(str(received[0:len(received)-2]))%255; #change this

			#if ((correctLen!=(len(received)-2)) or (correcthashVal!=hashVal)):
				#resend
			#	resendSignal()

			#else:

		for i in received[0:int(correctLen)]:
			song.append(str(i))
			if i==255:
				songEndCounter+=1;
		if songEndCounter==3:
			sendToFile()
			print("sent to file")
		signalCorrect()


		#else:
		#	print("error: not a multiple of 8")
		#	resendSignal()




if __name__ == "__main__":
    setup()
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
    GPIO.cleanup()
