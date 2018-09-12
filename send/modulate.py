import pigpio
import sys
import RPi.GPIO as GPIO

pi = pigpio.pi()
pi.set_mode(18, pigpio.OUTPUT)

pi.hardware_PWM(18, 38000, 500000)

while(1):
	try:
		i =1
	except KeyboardInterrupt:
		GPIO.cleanup()
		sys.exit(0)
