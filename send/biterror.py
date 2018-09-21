import numpy
import RPi.GPIO as GPIO
import time
import sys

#set up GPIO pin
LED_PIN = 22
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)


#start command
GPIO.output(22, True)
time.sleep(0.009)
GPIO.output(22,False)
time.sleep(0.0045)

toSend = []

for i in range (0, 250):
	#for j in range (0,i):
	toSend.append(0.0016)
	#for j in range(0,i):
	toSend.append(0.0005)
print(len(toSend))

for i in toSend:
	GPIO.output(22, True)
        time.sleep(0.0005)
        GPIO.output(22, False)
        time.sleep(i)

#stop command
GPIO.output(22, True)
time.sleep(0.05)
GPIO.output(22,False)
