from scene import Scene
from display import Display
import time
def main():
  # Settings
  CAMERA_NAME = "iPhone 15 Pro Max";
  CAMERA_FOV = 15.4
  CAMERA_ASPECT = .75
  PANO_FOV_X = 120 #degrees
  PANO_FOV_Y = 60 #degrees
  OVERLAP_PERCENT = .15 # whole number ex: 15 = 15 percent

  # Initialize and run
  display = Display()

  scene = Scene(CAMERA_FOV, CAMERA_ASPECT, CAMERA_NAME, PANO_FOV_X, PANO_FOV_Y, OVERLAP_PERCENT, display)
  scene.printInfo()
  time.sleep(3)
  scene.camera.printInfo();
  time.sleep(3)
  scene.runScene(250)
  display.clearLog()
if __name__ == "__main__":
    main()
    
    # main()