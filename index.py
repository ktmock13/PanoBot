#!/usr/bin/env python3
from scene import Scene
from menu import draw_menu, change_selection, menu_items
import RPi.GPIO as GPIO
import time

if __name__ == "__main__":
  try:  
    # Example sequence
    for _ in range(8):  # Repeat the block 9 times
        draw_menu()
        time.sleep(1)
        change_selection("down")
    time.sleep(2)
    sceneSettings =  {item['id']: item['value'] for item in menu_items if not item['id'].startswith("action")}
    scene = Scene(**sceneSettings)
    scene.runScene() 
    for _ in range(8):  # Repeat the block 9 times
        draw_menu()
        time.sleep(1)
        change_selection("up")
        GPIO.cleanup() # this ensures a clean exit  
    print("Goodbye!")
    time.sleep(2)
    scene.exitScene()
        # deactivate stepper/shutter relays

  except KeyboardInterrupt:  
     print('Exiting gracefully')  
  finally:
    # deactivate stepper/shutter relays
    GPIO.cleanup() # this ensures a clean exit  
    print("Goodbye!")