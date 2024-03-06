import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
GPIO.setmode(GPIO.BCM) 
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, 1) 
GPIO.output(24, 1)
