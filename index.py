#!/usr/bin/env python3
from scene import Scene
from menu import draw_menu, clear_screen, change_selection, menu_items, runMenu
import RPi.GPIO as GPIO
import time

if __name__ == "__main__":
  try:  
    runMenu()
  except KeyboardInterrupt:  
     print('Exiting gracefully')  
  finally:
    # deactivate stepper/shutter relays
    GPIO.cleanup() # this ensures a clean exit  
    print("Goodbye!")
    clear_screen()
