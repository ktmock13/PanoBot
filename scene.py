import math
import time
from robot import Robot
from camera import Camera
from display import Display
import RPi.GPIO as GPIO
from time import sleep
from RpiMotorLib import RpiMotorLib
import constants

class Shot:
  def __init__(self, x, y, height, width):
      self.x = x
      self.y = y
      self.height = height
      self.width = width
  def str(self):
      return f"x:{self.x} y:{self.y})"
class Scene:
    def __init__(self, cameraFOV, cameraAspectRatio, focusDelay, exposureDelay, rangeX, rangeY, overlapPercent, robotSpeed):
        self.running = False
        self.display = Display()
        # self.robot = Camera(cameraFOV, cameraAspect, cameraName, self.display)
        self.camera = Camera(cameraFOV, cameraAspectRatio)
        self.rangeX = rangeX  # total FOV degrees desired, ex. 100
        self.rangeY = rangeY  # total FOV degrees desired, ex. 50
        self.focusDelay = focusDelay
        self.exposureDelay = exposureDelay
        self.robotSpeed = robotSpeed
        self.shotSequence = []  # will be computed below
        # pins relevant to this class
        self.STEPPER_RELAY = 24
        # FOV units between shots, considering overlap
        xSpacing = (self.camera.getHorizontalFov() * (1 - overlapPercent))
        ySpacing = (self.camera.getVerticalFov() * (1 - overlapPercent))
        # Amount of FOV units that the shots overlap
        xOverlapAmount = (self.camera.getHorizontalFov() - xSpacing)
        yOverlapAmount = (self.camera.getVerticalFov() - ySpacing)
        # Min # of photos in each dimension to cover the desired range
        sceneDimensionX = math.ceil((rangeX - xOverlapAmount) / xSpacing)
        sceneDimensionY = math.ceil((rangeY - yOverlapAmount) / ySpacing)
        self.sceneDimensions = f'{sceneDimensionX}x{sceneDimensionY}'
        # All shots will be calculated from this frame of reference
        firstShot = Shot(0, 0, self.camera.getHorizontalFov(), self.camera.getVerticalFov())
        # Helper function to move to make new shots relative to a shot
        def createMovedShot(shot, xDistance, yDistance):
          return Shot(shot.x + xDistance, shot.y + yDistance, shot.height, shot.width)
        # generate all shots based on settings
        for iy in range(sceneDimensionY):
          #scan even rows LTR, odd rows RTL
          if iy % 2:
            for ix in reversed(range(sceneDimensionX)):
              # compute each shot
              self.shotSequence.append(createMovedShot(firstShot, ix * xSpacing, iy * ySpacing))
          else:
             for ix in range(sceneDimensionX):
              # compute each shot
              self.shotSequence.append(createMovedShot(firstShot, ix * xSpacing, iy * ySpacing))    
        # print shot count and sequence
        print('shot count: ', len(self.shotSequence))
        print('grid dimensions: ', self.sceneDimensions)
        print('shots generated')
        for shot in self.shotSequence:
          print(shot.str())
        GPIO.setup(self.STEPPER_RELAY, GPIO.OUT)

    def exitScene(self):
      self.running = False
      if constants.DEBUG != True:
        GPIO.output(self.STEPPER_RELAY, GPIO.LOW) # low is how you deactivate the relay
      # GPIO.cleanup()  # Clean up GPIO on CTRL+C exit

    def runScene(self):
      self.running = True
      #print scene dimensions 
      print(f"grid: {self.sceneDimensions}")

      self.display.loader(0, self.sceneDimensions)

      # activate stepper relay
      if constants.DEBUG != True:
        GPIO.output(self.STEPPER_RELAY, GPIO.LOW) #low is how you activate the relay

      # Init Robot
      robot = Robot(self.robotSpeed)
      # helper fn
      def timeout(ms):
        time.sleep(ms / 1000)

      #homing
      robot.centerToHome(self.rangeX, self.rangeY)

      # check for shot sequence
      if self.shotSequence and self.running:
          # loop through shots
          for index, shot in enumerate(self.shotSequence):
              # code to move
              robot.updatePosition(shot.x, shot.y);
              # delay to account for movement settle
              timeout(self.focusDelay)
              # code to take photo
              self.camera.capture()
              #increment loader screen
              self.display.loader((index + 1) / len(self.shotSequence) * 100, self.sceneDimensions)
              # delay to account for exposure
              timeout(self.exposureDelay)

      # deactivate stepper relay
      self.exitScene()
      self.display.clearLog()
