import RPi.GPIO as GPIO
import time

# Pin Definitions
up_button_pin = 17  # The GPIO pin the "Up" button is attached to
down_button_pin = 27  # The GPIO pin the "Down" button is attached to
select_button_pin = 22  # The GPIO pin the "Select" button is attached to

# Setup
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
GPIO.setup(up_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Up Button
GPIO.setup(down_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Down Button
GPIO.setup(select_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Select Button

# Dummy functions for menu actions
def function1():
    print("Function 1 executed")

def function2():
    print("Function 2 executed")

def function3():
    print("Function 3 executed")

# Menu items
menu_items = [function1, function2, function3]
current_item = 0  # Start at the first item

def up_callback(channel):
    global current_item
    current_item = (current_item - 1) % len(menu_items)
    print(f"Menu item {current_item+1}")

def down_callback(channel):
    global current_item
    current_item = (current_item + 1) % len(menu_items)
    print(f"Menu item {current_item+1}")

def select_callback(channel):
    menu_items[current_item]()  # Call the selected function

# Event Detection
GPIO.add_event_detect(up_button_pin, GPIO.FALLING, callback=up_callback, bouncetime=300)
GPIO.add_event_detect(down_button_pin, GPIO.FALLING, callback=down_callback, bouncetime=300)
GPIO.add_event_detect(select_button_pin, GPIO.FALLING, callback=select_callback, bouncetime=300)

try:
    print("Use Up/Down buttons to navigate the menu and Select to choose an option.")
    print(f"Menu item {current_item+1}")
    while True:
        # Do nothing, just wait for button events
        time.sleep(0.1)

except KeyboardInterrupt:
    # Clean up on Ctrl+C exit
    GPIO.cleanup()

GPIO.cleanup()  # Clean up at normal program exit
