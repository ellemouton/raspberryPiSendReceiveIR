import RPi.GPIO as GPIO
import math
import os
import numpy as np
import sys
from datetime import datetime
from time import sleep

INPUT_WIRE = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(INPUT_WIRE, GPIO.IN)

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

			if pulseLength.microseconds>50000:
				break

		previousVal = value
		value = GPIO.input(INPUT_WIRE)

	#get rid of start and stop commands and decode

	commandCut = ""

	for (val, pulse) in command[2:len(command)-1]:
                if val == 1:
			if pulse>1000:
				commandCut+="1"
			else:
				commandCut+="0"


	#split into groups of 8 (bytes)
	if(len(commandCut)%8==0):
		bytes = np.array_split(list(commandCut), len(commandCut)/8)

		#construct string for text file
		exportArr = []

		for b in bytes:
			exportArr.append(str(int("".join(b),2)))

		exportString = "["+",".join(exportArr)+"]"
		print(exportString)

		#write to text file
		f = open('interface2.txt','w')
        	f.write(exportString)
        	f.close()

	else:
		print("error: not a multiple of 8")

