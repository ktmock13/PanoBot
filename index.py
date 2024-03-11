#!/usr/bin/env python3
from scene import Scene
from menu import clear_screen, menu_items, run_menu
import RPi.GPIO as GPIO
import time

if __name__ == "__main__":
  try:  
    run_menu()
  except KeyboardInterrupt:  
     print('Exiting gracefully')  
  finally:
    # deactivate stepper/shutter relays
    GPIO.cleanup() # this ensures a clean exit  
    print("Goodbye!")
    clear_screen()
