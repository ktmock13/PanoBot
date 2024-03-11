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
    bar_width = self.display.width - 40  # Leave space for the text
    bar_height = 10  # Height of the loading bar
    bar_x = 10  # X-coordinate, 10 pixels from the left
    bar_y = (self.display.height // 2) + bar_height  # Position the bar in the middle of the display vertically

    # Draw the outline of the loading bar
    self.drawLog.rectangle([(bar_x, bar_y), (bar_x + bar_width, bar_y - bar_height)], outline=255, fill=0)

    # Calculate and draw the filled part of the loading bar
    fill_width = bar_width * (percent / 100)
    self.drawLog.rectangle([(bar_x, bar_y), (bar_x + fill_width, bar_y - bar_height)], outline=255, fill=255)

    # Create an image for the rotated text
    label = f"{percent}%"
    text_image = Image.new("1", (self.display.height, 20))  # Create a new image with enough height to accommodate rotated text
    draw_text = ImageDraw.Draw(text_image)
    draw_text.text((0, 0), label, font=self.font, fill=255)

    # Rotate the text image by 90 degrees
    rotated_text_image = text_image.rotate(90, expand=1)

    # Calculate the position to paste the rotated text image
    text_x = bar_x + bar_width + 10  # To the right of the loading bar, with a small gap
    text_y = (self.display.height - rotated_text_image.width) // 2  # Center the text image vertically

    # Paste the rotated text image onto the main image
    self.logImage.paste(rotated_text_image, (text_x, text_y))

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




       
      


        