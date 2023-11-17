import time
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

def _safe_access(array, index):
  try:
      return array[index]
  except IndexError:
      return ""
class Display:
  def __init__(self, isLogging = True):
    # Create the I2C interface.
    i2c = busio.I2C(SCL, SDA)
    self.display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

    # Clear display.
    self.display.fill(0)
    self.display.show()

    # Initialize an Image for logging purposes
    self.logImage = Image.new("1", (self.display.width, self.display.height))
    self.drawLog = ImageDraw.Draw(self.logImage)
    self.log = []

    # Initialize menu image
    self.menuImage = Image.new("1", (self.display.width, self.display.height))
    self.drawMenu = ImageDraw.Draw(self.menuImage)
    self.menu = ["a","b", "c", "d", "e"]


    # Get drawing object to draw on image.

    # Draw a black filled box to clear the image.
    self.isLogging = isLogging
    self.font = ImageFont.load_default()


    
  def printLog(self):
    # Draw a black filled box to clear the image.
    self.drawLog.rectangle((0, 0, self.display.width, self.display.height), outline=0, fill=0)
    # Write four lines of text.
    self.drawMenu.text((0,-2), self._safe_access(self.log, 3), font=self.font, fill=255)
    self.drawMenu.text((0,6), self._safe_access(self.log, 2), font=self.font, fill=255)
    self.drawMenu.text((0,14), self._safe_access(self.log, 1), font=self.font, fill=255)
    self.drawMenu.text((0,22), self._safe_access(self.log, 0), font=self.font, fill=255)

    # Display image.
    self.display.image(self.logImage)
    self.display.show()

  def log(self, text):
    self.log.append(text)
    self.printLog()

  def printMenu(self):
    # Draw a black filled box to clear the image.
    self.drawMenu.rectangle((0, 0, self.display.width, self.display.height), outline=0, fill=0)
    # Write four lines of text.
    self.drawMenu.text((0,-2), self._safe_access(self.menu, 3), font=self.font, fill=255)
    self.drawMenu.text((0,6), self._safe_access(self.menu, 2), font=self.font, fill=255)
    self.drawMenu.text((0,14), self._safe_access(self.menu, 1), font=self.font, fill=255)
    self.drawMenu.text((0,22), self._safe_access(self.menu, 0), font=self.font, fill=255)

    # Display image.
    self.display.image(self.menuImage)
    self.display.show()
    
  def toggleLog(self):
    self.isLogging = True
    self.printLog()

  def toggleMenu(self):
    self.isLogging = False
    self.printMenu()




       
      


        