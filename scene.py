import math
import time
from robot import Robot
from camera import Camera
from display import Display
import RPi.GPIO as GPIO
from time import sleep
from RpiMotorLib import RpiMotorLib

class Shot:
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
    def str(self):
        return f"x:{self.x} y:{self.y})"
class Scene:
    def __init__(self, cameraFOV, cameraAspect, cameraName, rangeX, rangeY, overlapPercent, display):
        self.display = display
        # self.robot = Camera(cameraFOV, cameraAspect, cameraName, self.display)
        self.camera = Camera(cameraFOV, cameraAspect, cameraName, self.display)
        self.rangeX = rangeX  # total FOV degrees desired, ex. 100
        self.rangeY = rangeY  # total FOV degrees desired, ex. 50
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
            for ix in range(sceneDimensionX):
              # compute each shot
              self.shotSequence.append(createMovedShot(firstShot, ix * xSpacing, iy * ySpacing))
          else:
             for ix in reversed(range(sceneDimensionX)):
              # compute each shot
              self.shotSequence.append(createMovedShot(firstShot, ix * xSpacing, iy * ySpacing))    
        GPIO.setup(self.STEPPER_RELAY, GPIO.OUT)

    def printInstructions(self):
        self.display.log('')
        self.display.log('  Connect BT Shutter...')
        self.display.log('')
        self.display.log('')

    def printInfo(self):
        self.display.log('Scene Info')
        self.display.log(f'-FOV: {self.rangeX}x{self.rangeY}')
        self.display.log(f'-Grid: {self.sceneDimensions}')
        self.display.log(f'-Shot Count: {len(self.shotSequence)}')

    def exitScene(self):
      GPIO.output(self.STEPPER_RELAY, GPIO.LOW) # low is how you deactivate the relay
      self.display.clearLog()

    def runScene(self, delay):
      # log info to display
      self.printInstructions()
      time.sleep(3)
      self.printInfo()
      time.sleep(3)
      self.camera.printInfo();
      time.sleep(3)

      # activate stepper relay
      GPIO.output(self.STEPPER_RELAY, GPIO.LOW) #low is how you activate the relay

      # Init Robot
      robot = Robot()
      # helper fn
      def timeout(ms):
          time.sleep(ms / 1000)

      # check for shot sequence
      if self.shotSequence:
          # loop through shots
          for shot in self.shotSequence:
              # code to move
              self.display.log(f'move..{shot.str()}')
              # robot.movePosition(shot.x, shot.y);
              timeout(delay)
              # code to take photo
              # self.camera.capture()
      # deactivate stepper relay
      self.exitScene()
      self.display.clearLog()
