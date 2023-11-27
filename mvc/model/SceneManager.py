import json

from mvc.model.scene import Scene

class SceneManager:
    def __init__(self):
        self.scenes = []

    def add_scene(self, scene):
        self.scenes.append(scene)

    def remove_scene(self, scene):
        self.scenes.remove(scene)

    def save_scenes(self, filename):
        scenes_json = [scene.to_dict() for scene in self.scenes]
        with open(filename, 'w') as f:
            json.dump(scenes_json, f)

    def load_scenes(self, filename):
        with open(filename, 'r') as f:
            scenes_json = json.load(f)
        self.scenes = [Scene.from_dict(scene_dict) for scene_dict in scenes_json]

    def log_scenes(self):
        for scene in self.scenes:
            print(scene.to_dict())