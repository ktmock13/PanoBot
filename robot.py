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
  def __init__(self):
    # states to track motor position
    self.currentXPosition = 0; # in degrees
    self.currentYPosition = 0; # in degrees
    # settings applied to both motors
    self.stepType = "1/16"
    self.stepDelay = .005;
    self.verboseOutput = True;
    self.initialDelay = .05;
    # settings applied to x motor
    self.X_DIR = 4
    self.X_STEP = 17
    self.Y_DIR = 27
    self.Y_STEP = 22
    self.SETTINGS = (14,15,18)
    # Declare a instance of class pass GPIO pins numbers and the motor type
    self.xMotor = RpiMotorLib.A4988Nema(self.X_DIR, self.X_STEP, self.SETTINGS, "A4988")
    self.yMotor = RpiMotorLib.A4988Nema(self.Y_DIR, self.Y_STEP, self.SETTINGS, "A4988")

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
      self.xMotor.motor_go(direction, # False=Clockwise, True=Counterclockwise
                         self.stepType, # Step type (Full,Half,1/4,1/8,1/16,1/32)
                         wholeNumberOfSteps, # number of steps
                         self.stepDelay, # step delay [sec]
                         self.verboseOutput, # True = print verbose output 
                         self.initialDelay) # initial delay [sec]
      self.currentXPosition = self.currentXPosition + actualAngleDifference;
    if desiredYPosition != self.currentYPosition:
      direction = self.currentYPosition < desiredYPosition # if current position is less than desired, move clockwise
      desiredAngleDifference = abs(self.currentYPosition - desiredYPosition)
      wholeNumberOfSteps = round(desiredAngleDifference / stepDegrees[self.stepType]);
      actualAngleDifference = wholeNumberOfSteps * stepDegrees[self.stepType]
      self.xMotor.motor_go(direction, # False=Clockwise, True=Counterclockwise
                         self.stepType, # Step type (Full,Half,1/4,1/8,1/16,1/32)
                         wholeNumberOfSteps, # number of steps
                         self.stepDelay, # step delay [sec]
                         self.verboseOutput, # True = print verbose output 
                         self.initialDelay) # initial delay [sec]
      self.currentYPosition = self.currentYPosition + actualAngleDifference;




       
      


        