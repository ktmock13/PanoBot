from scene import Scene
from display import Display
def main():
  # Settings
  CAMERA_NAME = "iPhone 15 Pro Max";
  CAMERA_FOV = 15.4
  CAMERA_ASPECT = .75
  PANO_FOV_X = 120 #degrees
  PANO_FOV_Y = 60 #degrees
  OVERLAP_PERCENT = .15 # whole number ex: 15 = 15 percent

  # Shot interval, time spent between snapshots
  SHOT_INTERVAL = 250 #milliseconds

  # Initialize and run
  scene = Scene(CAMERA_FOV, CAMERA_ASPECT, CAMERA_NAME, PANO_FOV_X, PANO_FOV_Y, OVERLAP_PERCENT)
  scene.runScene(SHOT_INTERVAL);


if __name__ == "__main__":
    main()
    # main()
