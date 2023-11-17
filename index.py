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
  scene = Scene(CAMERA_FOV, CAMERA_ASPECT, PANO_FOV_X, PANO_FOV_Y, OVERLAP_PERCENT, Display())
  scene.printInfo()
  scene.runScene(1000)

if __name__ == "__main__":
    main()
    
    # main()
