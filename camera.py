import RPi.GPIO as GPIO
import time
import constants

class Camera:
    def __init__(self, fovDegrees, aspectRatio, name, display):
      self.fovDegrees = fovDegrees  # assumed to be widest dimension of rectangle
      self.aspectRatio = aspectRatio
      self.isLandscape = aspectRatio >= 1
      self.name = name
      self.display = display
      # pins relevant to this class
      self.SHUTTER_RELAY = 23
      GPIO.setup(self.SHUTTER_RELAY, GPIO.OUT)

    def capture(self):
      if constants.DEBUG != True:
        GPIO.output(self.SHUTTER_RELAY, GPIO.LOW) # low is how you deactivate the relay
        time.sleep(.1)
        GPIO.output(self.SHUTTER_RELAY, GPIO.HIGH) # low is how you deactivate the relay

    def printInfo(self):
      self.display.log('Camera Info')
      self.display.log(f'-{self.name}')
      self.display.log(f'-FOV: {self.fovDegrees}')
      self.display.log(f'-Aspect: {self.aspectRatio} ({ "sq. " if self.aspectRatio == 1 else ("land." if self.isLandscape else "port.")})')

    def getHorizontalFov(self):
      # if this is a landscape photo, the self.fovDegrees value is the horizontal fov
      return self.fovDegrees if self.isLandscape else self.fovDegrees * self.aspectRatio

    def getVerticalFov(self):
      # if this is a portrait photo, the self.fovDegrees value is the vertical fov
      return self.fovDegrees if not self.isLandscape else self.fovDegrees * (1 / self.aspectRatio)
