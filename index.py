#!/usr/bin/env python3
from scene import Scene
import RPi.GPIO as GPIO
from constants import CAMERA_ASPECT, CAMERA_FOV, CAMERA_NAME, OVERLAP_PERCENT, PANO_FOV_X, PANO_FOV_Y, DELAY_BEFORE_SHOT, DELAY_AFTER_SHOT

if __name__ == "__main__":
  try:  
    scene = Scene(CAMERA_FOV, CAMERA_ASPECT, CAMERA_NAME, PANO_FOV_X, PANO_FOV_Y, OVERLAP_PERCENT)
    scene.runScene(DELAY_BEFORE_SHOT, DELAY_AFTER_SHOT) 
  except KeyboardInterrupt:  
     print('Exiting gracefully')  
  finally:
    # deactivate stepper/shutter relays
    GPIO.cleanup() # this ensures a clean exit  
    print("Goodbye!")