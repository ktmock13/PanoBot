import time
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

def _safe_access(array, index):
  try:
      return array[index]
  except IndexError:
      return " "
class Display:
  def __init__(self, isLogging = True):
    # Create the I2C interface.
    i2c = busio.I2C(SCL, SDA)
    self.display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

    # Clear display.
    # self.display.setRotation(2)
    self.display.fill(0)

    self.display.show()

    # Initialize an Image for logging purposes
    self.logImage = Image.new("1", (self.display.width, self.display.height))
    self.drawLog = ImageDraw.Draw(self.logImage)
    self.logList = []

    # Initialize menu image
    self.menuImage = Image.new("1", (self.display.width, self.display.height))
    self.drawMenu = ImageDraw.Draw(self.menuImage)
    self.menu = ["a","b", "c", "d", "e"]
    # Get drawing object to draw on image.

    # Draw a black filled box to clear the image.
    self.isLogging = isLogging
    self.font = ImageFont.load_default()

  def loader(self, percent):
    print(percent)
    # Clear the previous loader image
    self.drawLog.rectangle((0, 0, self.display.width, self.display.height), outline=0, fill=0)

    # Calculate the size and position of the loading bar
    bar_width = self.display.height - 20  # Use height for width due to rotation, with padding
    bar_height = 10  # Set the height of the loading bar
    bar_x = (self.display.width - bar_height) // 2  # Center the bar horizontally
    bar_y = 10  # Set y-coordinate to 10 pixels from the top (now the side)

    # Draw the outline of the loading bar
    self.drawLog.rectangle([(bar_x, bar_y), (bar_x + bar_height, bar_y + bar_width)], outline=255, fill=0)

    # Calculate and draw the filled part of the loading bar
    fill_width = bar_width * (percent / 100)
    self.drawLog.rectangle([(bar_x, bar_y), (bar_x + bar_height, bar_y + fill_width)], outline=255, fill=255)

    # Display the loading percentage label at the bottom of the screen (rotated)
    label = f"{percent}%"
    font = ImageFont.load_default()
    text_width, text_height = self.drawLog.textsize(label, font=font)

    # Because the screen is rotated, the label's x-coordinate is based on the display's width
    label_x = self.display.width - text_height - 1  # Subtract text_height to account for rotation
    label_y = (self.display.height - text_width) // 2  # Center the text along the display's height

    # Create a new image for the rotated text
    text_image = Image.new('1', (text_height, text_width))
    text_draw = ImageDraw.Draw(text_image)

    # Draw the text onto the text image
    text_draw.text((0, 0), label, font=font, fill=255)

    # Rotate the text image by 90 degrees to the right
    rotated_text_image = text_image.rotate(90, expand=1)

    # Paste the rotated text image onto the main image
    self.logImage.paste(rotated_text_image, (label_x, label_y))

    # Display the updated image on the OLED
    self.display.image(self.logImage)
    self.display.show()
    print(percent)
    # Clear the previous loader image
    self.drawLog.rectangle((0, 0, self.display.width, self.display.height), outline=0, fill=0)

    # Calculate the size and position of the loading bar
    bar_width = self.display.width - 20  # Subtract 10 pixels padding on each side
    bar_height = 10  # Set the height of the loading bar
    bar_x = 10  # Set x-coordinate to 10 pixels from the left
    bar_y = (self.display.height // 2) + bar_height  # Position the bar in the middle of the display vertically

    # Draw the outline of the loading bar
    self.drawLog.rectangle([(bar_x, bar_y), (bar_x + bar_width, bar_y - bar_height)], outline=255, fill=0)

    # Calculate and draw the filled part of the loading bar
    fill_width = bar_width * (percent / 100)
    self.drawLog.rectangle([(bar_x, bar_y), (bar_x + fill_width, bar_y - bar_height)], outline=255, fill=255)

    # Display the loading percentage label above the loading bar
    label = f"Loading: {percent}%"
    text_width, text_height = self.drawLog.textsize(label, font=self.font)
    label_x = (self.display.width - text_width) // 2  # Center the label
    label_y = bar_y - bar_height - 10 - text_height  # Position the label above the loading bar with a small gap
    self.drawLog.text((label_x, label_y), label, font=self.font, fill=255)

    # Display the updated image on the OLED
    self.display.image(self.logImage)
    self.display.show()

  def printLog(self):
    # Draw a black filled box to clear the image.
    self.drawLog.rectangle((0, 0, self.display.width, self.display.height), outline=0, fill=0)
    # Write four lines of text.
    self.drawLog.text((0,-2), _safe_access(self.logList, 3), font=self.font, fill=255)
    self.drawLog.text((0,6), _safe_access(self.logList, 2), font=self.font, fill=255)
    self.drawLog.text((0,14), _safe_access(self.logList, 1), font=self.font, fill=255)
    self.drawLog.text((0,22), _safe_access(self.logList, 0), font=self.font, fill=255)

    # Display image.
    self.display.image(self.logImage)
    self.display.show()

  def clearLog(self):
    self.logList = []
    self.log("")
    self.logList = []
    self.printLog()
    
  def log(self, text):
    self.logList.insert(0,text)
    self.printLog()

  def printMenu(self):
    # Draw a black filled box to clear the image.
    self.drawMenu.rectangle((0, 0, self.display.width, self.display.height), outline=0, fill=0)
    # Write four lines of text.
    self.drawMenu.text((0,-2), _safe_access(self.menu, 3), font=self.font, fill=255)
    self.drawMenu.text((0,6), _safe_access(self.menu, 2), font=self.font, fill=255)
    self.drawMenu.text((0,14), _safe_access(self.menu, 1), font=self.font, fill=255)
    self.drawMenu.text((0,22), _safe_access(self.menu, 0), font=self.font, fill=255)

    # Display image.
    self.display.image(self.menuImage)
    self.display.show()
    
  def toggleLog(self):
    self.isLogging = True
    self.printLog()

  def toggleMenu(self):
    self.isLogging = False
    self.printMenu()




       
      


        