from scene import Scene
from display import Display
import time
import RPi.GPIO as GPIO
from time import sleep

def main():
  # Settings
  CAMERA_NAME = "iPhone 15 Pro Max";
  CAMERA_FOV = 15.4
  CAMERA_ASPECT = .75
  PANO_FOV_X = 120 #degrees
  PANO_FOV_Y = 60 #degrees
  OVERLAP_PERCENT = .15 # whole number ex: 15 = 15 percent

  # Initialize and run
  display = Display()

  scene = Scene(CAMERA_FOV, CAMERA_ASPECT, CAMERA_NAME, PANO_FOV_X, PANO_FOV_Y, OVERLAP_PERCENT, display)
  scene.printInfo()
  time.sleep(3)
  scene.camera.printInfo();
  time.sleep(3)
  scene.runScene(250)
  display.clearLog()
if __name__ == "__main__":
  #this is the pin variable, change it if your relay is on a different pin
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(16, GPIO.OUT)
  GPIO.output(16, GPIO.HIGH)
  sleep(1)
  GPIO.output(16, GPIO.LOW)
  GPIO.cleanup()
  # main()