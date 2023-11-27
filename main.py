from modules.scene import Scene
from modules.display import Display
import time
def main():

  # Settings, these will be extraced from a data file later
  CAMERA_NAME = "iPhone 15 Pro Max";
  CAMERA_FOV = 15.4
  CAMERA_ASPECT = .75
  PANO_FOV_X = 120 #degrees
  PANO_FOV_Y = 60 #degrees
  OVERLAP_PERCENT = .15 # whole number ex: 15 = 15 percent


  # Initialize the display singleton class, this will be accesses throughout the code to control the screen
  display = Display()

  # Initialize a new scene with the test inputs above. Upon initiializing, this will perform the calculations to determine the shot sequence
  scene = Scene(CAMERA_FOV, CAMERA_ASPECT, CAMERA_NAME, PANO_FOV_X, PANO_FOV_Y, OVERLAP_PERCENT)

  # The following is a simple demonstration of some of the functions
  scene.printInfo()
  time.sleep(3)
  scene.camera.printInfo();
  time.sleep(3)
  scene.runScene(20)
  display.clearLog()

if __name__ == "__main__":
    main()
    
    # main()
