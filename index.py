#!/usr/bin/env python3
from scene import Scene
import RPi.GPIO as GPIO

# allow user to choose thsese
sceneSettings = {
  "cameraFOV": 15.4,
  "cameraAspectRatio": 0.75,
  "focusDelay": 0,
  "exposureDelay": 0,  # ms - to account for image exposure time required
  "rangeX": 120,  # degrees
  "rangeY": 60,   # degrees
  "overlapPercent": .30,
  "robotSpeed": 10 # 1-10
}

if __name__ == "__main__":
  try:  
    scene = Scene(**sceneSettings)
    scene.runScene() 
  except KeyboardInterrupt:  
     print('Exiting gracefully')  
  finally:
    # deactivate stepper/shutter relays
    GPIO.cleanup() # this ensures a clean exit  
    print("Goodbye!")