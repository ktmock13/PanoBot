#!/usr/bin/env python3
from scene import Scene
from menu import draw_menu, change_selection, menu_items
import RPi.GPIO as GPIO
import time

# allow user to choose thsese
sceneSettings = {
  "cameraFOV": 15.4,
  "cameraAspectRatio": 0.75,
  "focusDelay": 500,
  "exposureDelay": 500,  # ms - to account for image exposure time required
  "rangeX": 120,  # degrees
  "rangeY": 60,   # degrees
  "overlapPercent": .30,
  "robotSpeed": 5 # 1-10
}

if __name__ == "__main__":
  try:  
    # Example sequence
    for _ in range(8):  # Repeat the block 9 times
        draw_menu()
        time.sleep(1)
        change_selection("down")
    sceneSettings =  {item['id']: item['value'] for item in menu_items if not item['id'].startswith("action")}
    scene = Scene(**sceneSettings)
    scene.runScene() 
    for _ in range(8):  # Repeat the block 9 times
        draw_menu()
        time.sleep(1)
        change_selection("up")
    scene.exitScene()
  except KeyboardInterrupt:  
     print('Exiting gracefully')  
  finally:
    # deactivate stepper/shutter relays
    GPIO.cleanup() # this ensures a clean exit  
    print("Goodbye!")