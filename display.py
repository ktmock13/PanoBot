import time
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


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
    # Initialize log state
    self.log = ["11111111111111111111","22122222222222222222", "33333333333333333333", "44444444444444444444", "55555555555555555555555"]

    # Initialize menu image
    self.menuImage = Image.new("1", (self.display.width, self.display.height))
    self.menu = ["a","b", "c", "d", "e"]


    # Get drawing object to draw on image.
    self.draw = ImageDraw.Draw(self.logImage if isLogging else self.menuImage)

    # Draw a black filled box to clear the image.
    self.draw.rectangle((0, 0, self.display.width, self.display.height), outline=0, fill=0)
    self.isLogging = isLogging
    self.font = ImageFont.load_default()


  def printLog(self):
    # Draw a black filled box to clear the image.
    self.draw.rectangle((0, 0, self.display.width, self.display.height), outline=0, fill=0)
    # Write four lines of text.
    self.draw.text((0,-2), self.log[3], font=self.font, fill=255)
    self.draw.text((0,6), self.log[2], font=self.font, fill=255)
    self.draw.text((0,14), self.log[1], font=self.font, fill=255)
    self.draw.text((0,22), self.log[0], font=self.font, fill=255)

    # Display image.
    self.display.image(self.logImage)
    self.display.show()

  def printMenu(self):
    # Draw a black filled box to clear the image.
    self.draw.rectangle((0, 0, self.display.width, self.display.height), outline=0, fill=0)
    # Write four lines of text.
    self.draw.text((0,-2), self.menu[3], font=self.font, fill=255)
    self.draw.text((0,6), self.menu[2], font=self.font, fill=255)
    self.draw.text((0,14), self.menu[1], font=self.font, fill=255)
    self.draw.text((0,22), self.menu[0], font=self.font, fill=255)

    # Display image.
    self.display.image(self.logImage)
    self.display.show()
    
  def toggleLog(self):
    self.isLogging = True
    self.printLog()

  def toggleMenu(self):
    self.isLogging = True
    self.printLog()




       
      


        