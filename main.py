from mvc.controller.SceneController import SceneController

# Settings, these will be extraced from a data file later
CAMERA_FOV = 15.4
CAMERA_ASPECT = .75
PANO_FOV_X = 120 #degrees
PANO_FOV_Y = 60 #degrees
OVERLAP_PERCENT = .15 # whole number ex: 15 = 15 percent

def main():
    # Initialize the controller
    controller = SceneController()
    controller.load_scenes("scenes.json")

    controller.log_scenes();

    
    # Use the controller to manage scenes
    controller.create_scene(15.4, .75, 120, 60, .15)
    controller.create_scene(9, 1, 90, 40, .2)
    controller.save_scenes("scenes.json")

if __name__ == "__main__":
    main()