import time
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import constants
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
  def __init__(self, speed):
    # states to track motor position
    self.currentXPosition = 0; # in degrees
    self.currentYPosition = 0; # in degrees
    # settings applied to both motors
    self.stepType = "1/16"
    self.stepDelay = max(0.001, min(0.01, (abs(speed-11) * 0.001))); #0.005 is the perfect speed for the stepper motor, this param allows for adjustment while limiting the range
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

  def centerToHome(self, xFOV,yFOV):
    # theoretical center
    xPosition = xFOV / 2
    yPosition = yFOV / 2
    wholeNumberOfXSteps = round(abs(xPosition - 0) / stepDegrees[self.stepType]);
    wholeNumberOfYSteps = round(abs(yPosition - 0) / stepDegrees[self.stepType]);
    self.xMotor.motor_go(False, # False=Clockwise, True=Counterclockwise
                      self.stepType, # Step type (Full,Half,1/4,1/8,1/16,1/32)
                      wholeNumberOfXSteps, # number of steps
                      self.stepDelay, # step delay [sec]
                      self.verboseOutput, # True = print verbose output 
                      self.initialDelay) # initial delay [sec]
    self.yMotor.motor_go(False, # False=Clockwise, True=Counterclockwise
                      self.stepType, # Step type (Full,Half,1/4,1/8,1/16,1/32)
                      wholeNumberOfYSteps, # number of steps
                      self.stepDelay, # step delay [sec]
                      self.verboseOutput, # True = print verbose output 
                      self.initialDelay) # initial delay [sec]

  # this will get the axis as close to the desiredPosition as possible with the stepType units
  def updatePosition(self, desiredXPosition, desiredYPosition):
    if desiredXPosition != self.currentXPosition:
      print(f'moving x from {self.currentXPosition} to {desiredXPosition}')
      direction = self.currentXPosition < desiredXPosition # if current position is less than desired, move clockwise
      desiredAngleDifference = abs(self.currentXPosition - desiredXPosition)
      wholeNumberOfSteps = round(desiredAngleDifference / stepDegrees[self.stepType]);
      actualAngleDifference = wholeNumberOfSteps * stepDegrees[self.stepType]
      if constants.DEBUG != True:
        self.xMotor.motor_go(direction, # False=Clockwise, True=Counterclockwise
                          self.stepType, # Step type (Full,Half,1/4,1/8,1/16,1/32)
                          wholeNumberOfSteps, # number of steps
                          self.stepDelay, # step delay [sec]
                          self.verboseOutput, # True = print verbose output 
                          self.initialDelay) # initial delay [sec]
      # since X oscillates, we need to account for that
      if direction: # increasing (left to right)
        self.currentXPosition = self.currentXPosition + actualAngleDifference;
      else: # decreasing (right to left)
        self.currentXPosition = self.currentXPosition - actualAngleDifference;
      print(f'new x position {self.currentXPosition}')
    if desiredYPosition != self.currentYPosition:
      print(f'moving y from {self.currentYPosition} to {desiredYPosition}')
      direction = self.currentYPosition < desiredYPosition # if current position is less than desired, move clockwise
      desiredAngleDifference = abs(self.currentYPosition - desiredYPosition)
      wholeNumberOfSteps = round(desiredAngleDifference / stepDegrees[self.stepType]);
      actualAngleDifference = wholeNumberOfSteps * stepDegrees[self.stepType]
      if constants.DEBUG != True:
        self.yMotor.motor_go(direction, # False=Clockwise, True=Counterclockwise
                          self.stepType, # Step type (Full,Half,1/4,1/8,1/16,1/32)
                          wholeNumberOfSteps, # number of steps
                          self.stepDelay, # step delay [sec]
                          self.verboseOutput, # True = print verbose output 
                          self.initialDelay) # initial delay [sec]
      self.currentYPosition = self.currentYPosition + actualAngleDifference; # y direction only increases
      print(f'new y position {self.currentYPosition}')






       
      


        