from scene import Scene
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import RPi.GPIO as GPIO
import time

screen_width, screen_height = 32, 128  # Screen dimensions

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)
display = adafruit_ssd1306.SSD1306_I2C(screen_height, screen_width, i2c)
display.rotation = 0  # Adjust rotation as needed
display.fill(0)
display.show()


# Menu items definition
menu_items = [
    {"id": "cameraFOV", "value": 15.5, "increment": 0.5},
    {"id": "cameraAspectRatio", "value": 0.75, "increment": 0.5},
    {"id": "focusDelay", "value": 500, "increment": 100},
    {"id": "exposureDelay", "value": 500, "increment": 100},
    {"id": "rangeX", "value": 120, "increment": 5},
    {"id": "rangeY", "value": 60, "increment": 5},
    {"id": "overlapPercent", "value": 0.3, "increment": 0.05},
    {"id": "robotSpeed", "value": 7, "increment": 1},
    # Add more menu items as needed
    {"id": "action-start", "value": "START"}  # 'START' as the last menu item
]

# Initial state
selected_index = 8
editing_mode = False

# Create an image with PIL
image = Image.new("1", (screen_width, screen_height), "black")
# image = image.rotate(90, expand=True)
draw = ImageDraw.Draw(image)
# font_path = "ret.ttf"  # Update this to your font's path
# font_size = 6
# font = ImageFont.truetype(font_path, font_size)
font = ImageFont.load_default()  # Default font, adjust as needed
print(font.getsize("hello"))

def draw_menu():
    draw.rectangle((0, 0, screen_width, screen_height), fill="black")  # Clear screen

    for index, item in enumerate(menu_items):
        # Skip non-selected items if in editing mode
        if editing_mode and index != selected_index:
            continue

        text = str(item["value"])
        text_width, text_height = draw.textsize(text, font=font)

        # Keep the y position calculation consistent regardless of editing mode
        y = 3 + index * (screen_height // len(menu_items))

        if index == selected_index:
            # Highlight selected item: draw a white rectangle behind the text
            draw.rectangle((0, y, screen_width, y + text_height), fill="white")
            draw.text((2, y), text, font=font, fill="black")
        else:
            draw.text((2, y), text, font=font, fill="white")

    rotated_image = image.rotate(90, expand=True)
    display.image(rotated_image)
    display.show()


def clear_screen():
    display.image(Image.new("1", (screen_width, screen_height), "black"))
    display.show()

def change_selection(direction):
    global selected_index
    if direction == "up" and selected_index > 0:
        selected_index -= 1
    elif direction == "down" and selected_index < len(menu_items) - 1:
        selected_index += 1
    draw_menu()

def toggle_editing_mode():
    global editing_mode
    editing_mode = not editing_mode
    print("Editing mode:", editing_mode)
    draw_menu()

def adjust_value(direction):
    if "increment" in menu_items[selected_index]:  # Check if the item is adjustable
        increment = menu_items[selected_index]["increment"]
        if direction == "up":
            menu_items[selected_index]["value"] += increment
        elif direction == "down":
            menu_items[selected_index]["value"] -= increment
        menu_items[selected_index]["value"] = round(menu_items[selected_index]["value"], 2)  # Adjust rounding precision
    draw_menu()

def long_task():
    print("Starting...")  # Or perform the start action
    sceneSettings =  {item['id']: item['value'] for item in menu_items if not item['id'].startswith("action")}
    scene = Scene(**sceneSettings)
    scene.runScene() 
def run_menu():
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Up button
    GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Select button
    GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Down button
    draw_menu()
    def up_callback(channel):
        def action():
          global selected_index, editing_mode
          if editing_mode and "increment" in menu_items[selected_index]:
              # Increase the value in editing mode
              menu_items[selected_index]["value"] += menu_items[selected_index]["increment"]
              menu_items[selected_index]["value"] = round(menu_items[selected_index]["value"], 2)  # Maintain 2 decimal places
              draw_menu()
          elif not editing_mode and selected_index > 0:
              # Move selection up in navigation mode
              selected_index -= 1
              draw_menu()
        # action()
        while GPIO.input(16) == GPIO.LOW:  # While button is still pressed
          # Here you would trigger your 'click' action
          action()
          time.sleep(0.12)  # Wait 250ms before the next action

    def down_callback(channel):
      def action():
        global selected_index, editing_mode
        if editing_mode and "increment" in menu_items[selected_index]:
          # Decrease the value in editing mode
          menu_items[selected_index]["value"] -= menu_items[selected_index]["increment"]
          menu_items[selected_index]["value"] = round(menu_items[selected_index]["value"], 2)  # Maintain 2 decimal places
          draw_menu()
        elif not editing_mode and selected_index < len(menu_items) - 1:
          # Move selection down in navigation mode
          selected_index += 1
          draw_menu()
      # action()
      while GPIO.input(21) == GPIO.LOW:  # While button is still pressed
        # Here you would trigger your 'click' action
        action()
        time.sleep(0.12)  # Wait 250ms before the next action
        

    def select_callback(channel):
        global editing_mode
        if menu_items[selected_index]["value"] == "START":
            long_task()
        elif not editing_mode:
            toggle_editing_mode()
        else:
            toggle_editing_mode()

    # Define the button press event callbacks
    GPIO.add_event_detect(16, GPIO.FALLING, callback=up_callback, bouncetime=300)
    GPIO.add_event_detect(20, GPIO.FALLING, callback=select_callback, bouncetime=300)
    GPIO.add_event_detect(21, GPIO.FALLING, callback=down_callback, bouncetime=300)
    try:
        while True:
            time.sleep(0.1)  # Small delay to reduce CPU usage
    except KeyboardInterrupt:
        GPIO.cleanup()  # Clean up GPIO on CTRL+C exit
        clear_screen()

