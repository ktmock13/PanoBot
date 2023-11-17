from scene import Scene
from display import Display
import time
def main():
  # Settings
  CAMERA_FOV = 15.4
  CAMERA_ASPECT = .75
  PANO_FOV_X = 120 #degrees
  PANO_FOV_Y = 60 #degrees
  OVERLAP_PERCENT = .15 # whole number ex: 15 = 15 percent

  # Initialize and run
  scene = Scene(CAMERA_FOV, CAMERA_ASPECT, PANO_FOV_X, PANO_FOV_Y, OVERLAP_PERCENT)
  scene.printInfo()
  scene.runScene(1000)

if __name__ == "__main__":
    display = Display()
    display.toggleLog()
    time.sleep(1)
    display.log("ok")
    print(display.log)
    time.sleep(1)
    display.log("this")
    time.sleep(1)
    display.log("is")
    time.sleep(1)
    display.log("working")
    time.sleep(1)
    display.log("well")
    time.sleep(1)   
    display.toggleMenu()
    time.sleep(1)
    display.toggleLog()
    time.sleep(1)
    display.toggleMenu()
    time.sleep(1)
    
    # main()
