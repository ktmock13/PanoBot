import time
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

#how many degrees the step type moves
stepDegrees = {
  'Full': 1.8,
  'Half': 0.9,
  '1/4': 0.45,
  '1/8': 0.225,
  '1/16': 0.1125,
  '1/32': 0.05625
}

class Robot:
  def __init__(self, stepsPerRotation, move):
    # states to track motor position
    self.currentXPosition = 0; # in degrees
    self.currentYPosition = 0; # in degrees
    self.stepType = "1/4"
    ################################
    # RPi and Motor Pre-allocations
    ################################
    
    # Declare a instance of class pass GPIO pins numbers and the motor type
    self.xmotor = RpiMotorLib.A4988Nema(19, 26, (5,6,13), "DRV8825")
    self.ymotor = RpiMotorLib.A4988Nema(16, 20, (5,6,13), "DRV8825")

    GPIO.setup(24,GPIO.OUT) # set enable pin as output

  def capture(self):
    print('capture')
  def getPosition(self, axis):
    if axis == 'x':
      return self.currentXPosition
    elif axis == 'y':
      return self.currentYPosition
    else: 
      print('invalid axis')

  # this will get the axis as close to the desiredPosition as possible with the stepType units
  def movePosition(self, desiredXPosition, desiredYPosition):
    if desiredXPosition != self.currentXPosition:
      direction = self.currentXPosition < desiredXPosition # if current position is less than desired, move clockwise
      desiredAngleDifference = abs(self.currentXPosition - desiredXPosition)
      wholeNumberOfSteps = round(desiredAngleDifference / stepDegrees[self.stepType]);
      actualAngleDifference = wholeNumberOfSteps * stepDegrees[self.stepType]
      self.xmotor.motor_go(direction, # False=Clockwise, True=Counterclockwise
                         self.stepType, # Step type (Full,Half,1/4,1/8,1/16,1/32)
                         wholeNumberOfSteps, # number of steps
                         .01, # step delay [sec]
                         True, # True = print verbose output 
                         .05) # initial delay [sec]
      self.currentXPosition = self.currentXPosition + actualAngleDifference;
    if desiredYPosition != self.currentYPosition:
      direction = self.currentYPosition < desiredYPosition # if current position is less than desired, move clockwise
      desiredAngleDifference = abs(self.currentYPosition - desiredYPosition)
      wholeNumberOfSteps = round(desiredAngleDifference / stepDegrees[self.stepType]);
      actualAngleDifference = wholeNumberOfSteps * stepDegrees[self.stepType]
      self.ymotor.motor_go(direction, # False=Clockwise, True=Counterclockwise
                         self.stepType, # Step type (Full,Half,1/4,1/8,1/16,1/32)
                         wholeNumberOfSteps, # number of steps
                         .01, # step delay [sec]
                         True, # True = print verbose output 
                         .05) # initial delay [sec]
      self.currentYPosition = self.currentYPosition + actualAngleDifference;




       
      


        