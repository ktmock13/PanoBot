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

# Setup inpuot buttons
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Up button
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Select button
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Down button

# Menu items definition
menu_items = [
    {"id": 1, "value": 8.75, "increment": 0.5},
    {"id": 2, "value": 15.4, "increment": 1.0},
    {"id": 3, "value": 500, "increment": 5.0},
    {"id": 4, "value": 250, "increment": 10.0},
    {"id": 5, "value": 128, "increment": 2.0},
    {"id": 6, "value": 68, "increment": 0.1},
    {"id": 7, "value": "START"}
]

# Initial state
selected_index = 0
editing_mode = False

# Create an image with PIL
screen_width, screen_height = 128, 160  # Screen dimensions
image = Image.new("RGB", (screen_width, screen_height), "black")
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()  # Default font, adjust as needed

def draw_menu():
    draw.rectangle((0, 0, screen_width, screen_height), fill="black")  # Clear screen
    for index, item in enumerate(menu_items):
        text = str(item["value"])
        text_width, text_height = draw.textsize(text, font=font)
        if item["value"] == "START":
            x = (screen_width - text_width) / 2  # Center 'START' horizontally
        else:
            x = 5  # Regular items aligned to the left

        y = 10 + index * (screen_height // len(menu_items))
        if index == selected_index:
            draw.rectangle((0, y, screen_width, y + text_height + 5), fill="white")
            draw.text((x, y), text, font=font, fill="black")
        else:
            draw.text((x, y), text, font=font, fill="white")

    image.show()  # Display the image, replace with your display method

def up_callback(channel):
    global selected_index
    if selected_index > 0:
        selected_index -= 1
        draw_menu()

def down_callback(channel):
    global selected_index
    if selected_index < len(menu_items) - 1:
        selected_index += 1
        draw_menu()

def select_callback(channel):
    global editing_mode, selected_index
    if menu_items[selected_index]["value"] == "START":
        print("Starting...")  # Or perform the start action
        sceneSettings =  {item['id']: item['value'] for item in menu_items if not item['id'].startswith("action")}
        scene = Scene(**sceneSettings)
        scene.runScene() 
    elif not editing_mode:
        editing_mode = True
    else:
        editing_mode = False
    draw_menu()

# Define the button press event callbacks
GPIO.add_event_detect(16, GPIO.FALLING, callback=up_callback, bouncetime=300)
GPIO.add_event_detect(20, GPIO.FALLING, callback=select_callback, bouncetime=300)
GPIO.add_event_detect(21, GPIO.FALLING, callback=down_callback, bouncetime=300)

# Initial draw
draw_menu()

# Keep the script running to listen for button inputs
try:
    while True:
        time.sleep(0.1)  # Small delay to reduce CPU usage
except KeyboardInterrupt:
    GPIO.cleanup()  # Clean up GPIO on CTRL+C exit