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
    # calculate the size and position of the loading bar
    bar_width = self.display.width * 0.8  # set width to 80% of the display's width
    bar_height = self.display.height * 0.8  # set height to 80% of the display's height
    bar_x = self.display.width * 0.1  # set x-coordinate to 10% of the display's width
    bar_y = self.display.height  # set y-coordinate to the display's height
    # draw the outline of the loading bar
    self.drawLog.rectangle([(bar_x, bar_y), (bar_x + bar_width, bar_y - bar_height)], outline=255, fill=0)  # adjusted y-coordinates to flip the bar
    # calculate the filled part of the loading bar
    fill_width = bar_width * percent / 100
    # draw the filled part of the loading bar
    self.drawLog.rectangle([(bar_x, bar_y), (bar_x + fill_width, bar_y - bar_height)], outline=255, fill=255)  # adjusted y-coordinates to flip the bar
    # Display image.
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
    self.log("log cleared")
    time.sleep(1)
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




       
      


        