#!/usr/bin/env python3
from scene import Scene
from menu import clear_screen, menu_items, run_menu
import RPi.GPIO as GPIO

if __name__ == "__main__":
  try:
    GPIO.setmode(GPIO.BCM)
    run_menu()
  except KeyboardInterrupt:  
     print('Exiting gracefully')  
  finally:
    # deactivate stepper/shutter relays
    GPIO.cleanup() # this ensures a clean exit  
    print("Goodbye!")
    clear_screen()
