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

  def loader(self, percent, label="11x5"):
    print(percent)
    # calculate the size and position of the loading bar
    bar_width = self.display.width - 20  # subtract 10 pixels from the display's width for padding
    bar_height = self.display.height -5 # subtract 20 pixels from the display's height for padding and label space
    bar_x = 5  # set x-coordinate to 5 pixels for padding
    bar_y = 0  # set y-coordinate to 15 pixels for padding

    # draw the outline of the loading bar
    self.drawLog.rectangle([(bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height)], outline=255, fill=0)
    
    # calculate the filled part of the loading bar
    fill_width = bar_width * percent / 100

    # draw the filled part of the loading bar
    self.drawLog.rectangle([(bar_x + bar_width-fill_width, bar_y), (bar_x + bar_width, bar_y + bar_height)], outline=255, fill=255)

    # Create an image for the label
    label_image = Image.new("1", (bar_height, self.font.getsize(label)[1]))  # Create a new image with height of the bar and width of the text
    label_draw = ImageDraw.Draw(label_image)

    # Draw the label text onto the label image
    label_draw.text((0, 0), label, font=self.font, fill=255)

    # Rotate the label image by 90 degrees
    rotated_label = label_image.rotate(90, expand=True)

    # Paste the rotated label image onto the logImage
    self.logImage.paste(rotated_label, (self.display.width - rotated_label.width, bar_y))

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




       
      


        