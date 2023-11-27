from mvc.model.SceneManager import SceneManager
from mvc.model.scene import Scene

class SceneController:
  def __init__(self):
    self.scene_manager = SceneManager()

  def create_scene(self,  cameraFOV, cameraAspect, rangeX, rangeY, overlapPercent):
    scene = Scene(cameraFOV, cameraAspect, rangeX, rangeY, overlapPercent)
    self.scene_manager.add_scene(scene)

  def save_scenes(self, filename):
    self.scene_manager.save_scenes(filename)

  def load_scenes(self, filename):
    self.scene_manager.load_scenes(filename)

  def log_scenes(self):
    self.scene_manager.log_scenes()