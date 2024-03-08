from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


screen_width, screen_height = 32, 128  # Screen dimensions

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)
display = adafruit_ssd1306.SSD1306_I2C(screen_height, screen_width, i2c)
display.rotation = 0  # Adjust rotation as needed
display.fill(0)
display.show()


# Menu items definition
menu_items = [
    {"id": 1, "value": 0.75, "increment": 0.5},
    {"id": 2, "value": 15.5, "increment": 0.5},
    {"id": 3, "value": 500, "increment": 100},
    {"id": 4, "value": 500, "increment": 100},
    {"id": 5, "value": 120, "increment": 5},
    {"id": 6, "value": 60, "increment": 5},
    {"id": 7, "value": 0.3, "increment": 0.05},
    # Add more menu items as needed
    {"id": 7, "value": "START"}  # 'START' as the last menu item
]

# Initial state
selected_index = 0
editing_mode = False

# Create an image with PIL
image = Image.new("1", (screen_width, screen_height), "black")
# image = image.rotate(90, expand=True)
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()  # Default font, adjust as needed
print(font.getsize())

def draw_menu():
    draw.rectangle((0, 0, screen_width, screen_height), fill="black")  # Clear screen

    for index, item in enumerate(menu_items):
        text = str(item["value"])
        text_width, text_height = draw.textsize(text, font=font)
        
        # Calculate y position based on index, adjust as needed
        y = 4 + index * (screen_height // len(menu_items))
        
        if index == selected_index:
            # Highlight selected item: draw a white rectangle behind the text
            draw.rectangle((0, y, screen_width, y + text_height), fill="white")
            draw.text((5, y), text, font=font, fill="black")
        else:
            draw.text((5, y), text, font=font, fill="white")

    rotated_image = image.rotate(90, expand=True)

    display.image(rotated_image)
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

# Initial draw
draw_menu()

# # Example interaction (replace with actual GPIO button handling)
# try:
#     while True:
#         command = input("Enter command (up, down, select, edit): ").lower()
#         if command == "up":
#             change_selection("up")
#         elif command == "down":
#             change_selection("down")
#         elif command == "select":
#             if menu_items[selected_index]["value"] == "START":
#                 print("Starting...")
#             elif not editing_mode:
#                 toggle_editing_mode()
#             else:
#                 toggle_editing_mode()
#         elif command == "edit" and editing_mode:
#             adjust_value("up")  # Example adjustment, replace with actual button input
# except KeyboardInterrupt:
#     print("Program exited")
