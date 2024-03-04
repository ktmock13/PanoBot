import math
import time
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
        return f"Shot at ({self.x}, {self.y}), Height: {self.height}, Width: {self.width}"

class Camera:
    def __init__(self, fovDegrees, aspectRatio, name, display):
        self.fovDegrees = fovDegrees  # assumed to be widest dimension of rectangle
        self.aspectRatio = aspectRatio
        self.isLandscape = aspectRatio >= 1
        self.name = name
        self.display = display
        # calculate shotHeight and shotWidth based on fov and aspect

    def printInfo(self):
        self.display.log('Camera Info')
        self.display.log(f'- {self.name}')
        self.display.log(f'- Lens FOV: {self.fovDegrees}')
        self.display.log(f'- Lens Aspect: {self.aspectRatio} ({ "sq. " if self.aspectRatio == 1 else ("land." if self.isLandscape else "port.")})')

    def getHorizontalFov(self):
        # if this is a landscape photo, the self.fovDegrees value is the horizontal fov
        return self.fovDegrees if self.isLandscape else self.fovDegrees * self.aspectRatio

    def getVerticalFov(self):
        # if this is a portrait photo, the self.fovDegrees value is the vertical fov
        return self.fovDegrees if not self.isLandscape else self.fovDegrees * (1 / self.aspectRatio)

class Scene:
    def __init__(self, cameraFOV, cameraAspect, cameraName, rangeX, rangeY, overlapPercent, display):
        self.display = display
        self.camera = Camera(cameraFOV, cameraAspect, cameraName, self.display)
        self.rangeX = rangeX  # total FOV degrees desired, ex. 100
        self.rangeY = rangeY  # total FOV degrees desired, ex. 50
        self.shotSequence = []  # will be computed below
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
              

    def printInfo(self):
        self.display.log('Scene Info')
        self.display.log(f'- Pano FOV: {self.rangeX}x{self.rangeY}')
        self.display.log(f'- Pano Grid: {self.sceneDimensions}')
        self.display.log(f'- # of shots: {len(self.shotSequence)}')

    def runScene(self, delay):
      GPIO.setup(24, GPIO.OUT)
      GPIO.setup(23, GPIO.OUT)

      GPIO.output(24, 0)

      #TBD initialize real robot
      xmotor = RpiMotorLib.A4988Nema(4, 17, (14,15,18), "A4988")
      ymotor = RpiMotorLib.A4988Nema(27, 22, (14,15,18), "A4988")

      self.printInfo()
      time.sleep(3)
      self.camera.printInfo();
      time.sleep(3) 
      def timeout(ms):
          time.sleep(ms / 1000)
      if self.shotSequence:
          for shot in self.shotSequence:
              # code to move, use current shot
              self.display.log(f'move..{shot.str()}')
              xmotor.motor_go(True, # False=Clockwise, True=Counterclockwise
                         "1/16" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                         40, # number of steps
                         .005, # step delay [sec]
                         True, # True = print verbose output 
                         .05) # initial delay [sec]
              ymotor.motor_go(True, # False=Clockwise, True=Counterclockwise
                         "1/16" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                         40, # number of steps
                         .005, # step delay [sec]
                         True, # True = print verbose output 
                         .05) # initial delay [sec]
              timeout(delay / 2)
              # code to take photo
              self.display.log('capture... ')
              GPIO.output(23, 0)
              time.sleep(.1)
              GPIO.output(23, 1)
              timeout(delay / 2)
      self.display.clearLog()