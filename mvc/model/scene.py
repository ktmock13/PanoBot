import math

class Shot:
  def __init__(self, x, y, height, width):
      self.x = x
      self.y = y
      self.height = height
      self.width = width
  def to_dict(self):
        return {
            'x': self.x,
            'y': self.y,
            'height': self.height,
            'width': self.width
        }

  @staticmethod
  def from_dict(shot_dict):
      return Shot(
          x=shot_dict['x'],
          y=shot_dict['y'],
          height=shot_dict['height'],
          width=shot_dict['width']
      )

class Camera:
  def __init__(self, fovDegrees, aspectRatio, name):
    self.fovDegrees = fovDegrees  # assumed to be widest dimension of rectangle
    self.aspectRatio = aspectRatio
    self.isLandscape = aspectRatio >= 1
    self.name = name
    # calculate shotHeight and shotWidth based on fov and aspect

  def getHorizontalFov(self):
    # if this is a landscape photo, the self.fovDegrees value is the horizontal fov
    return self.fovDegrees if self.isLandscape else self.fovDegrees * self.aspectRatio

  def getVerticalFov(self):
    # if this is a portrait photo, the self.fovDegrees value is the vertical fov
    return self.fovDegrees if not self.isLandscape else self.fovDegrees * (1 / self.aspectRatio)
  def to_dict(self):
      return {
          'fovDegrees': self.fovDegrees,
          'aspectRatio': self.aspectRatio,
          'name': self.name,
          'isLandscape': self.isLandscape
      }

  @staticmethod
  def from_dict(camera_dict):
      return Camera(
          fovDegrees=camera_dict['fovDegrees'],
          aspectRatio=camera_dict['aspectRatio'],
          name=camera_dict['name']
      )
class Scene:
  def __init__(self, cameraFOV, cameraAspect, rangeX, rangeY, overlapPercent):
    self.camera = Camera(cameraFOV, cameraAspect, "default")
    self.rangeX = rangeX  # total FOV degrees desired, ex. 100
    self.rangeY = rangeY  # total FOV degrees desired, ex. 50
    self.shotSequence = []  # will be computed below
    # FOV units between shots, considering overlap
    xSpacing = (self.camera.getHorizontalFov() * (1 - overlapPercent))
    ySpacing = (self.camera.getVerticalFov() * (1 - overlapPercent))
    # Amount of FOV units that the shots overlap
    xOverlapAmount = (self.camera.getHorizontalFov() - xSpacing)
    yOverlapAmount = (self.camera.getVerticalFov() - ySpacing)
    # Min # of photos in each dimension to cover the desired range
    sceneDimensionX = math.ceil((rangeX - xOverlapAmount) / xSpacing)
    sceneDimensionY = math.ceil((rangeY - yOverlapAmount) / ySpacing)
    self.sceneDimensions = f'{sceneDimensionX}x{sceneDimensionY}'
    
    # All shots will be calculated from this frame of reference
    firstShot = Shot(0, 0, self.camera.getHorizontalFov(), self.camera.getVerticalFov())
    # Helper function to move to make new shots relative to a shot
    def createMovedShot(shot, xDistance, yDistance):
        return Shot(shot.x + xDistance, shot.y + yDistance, shot.height, shot.width)
    for iy in range(sceneDimensionY):
        for ix in range(sceneDimensionX):
            # compute each shot
            self.shotSequence.append(createMovedShot(firstShot, ix * xSpacing, iy * ySpacing))
  def to_dict(self):
    return {
        'cameraFOV': self.camera.fovDegrees,
        'cameraAspect': self.camera.aspectRatio,
        'rangeX': self.rangeX,
        'rangeY': self.rangeY,
        'overlapPercent': self.overlapPercent,
        'shotSequence': [shot.to_dict() for shot in self.shotSequence]
    }

  @staticmethod
  def from_dict(scene_dict):
    scene = Scene(
        cameraFOV=scene_dict['cameraFOV'],
        cameraAspect=scene_dict['cameraAspect'],
        rangeX=scene_dict['rangeX'],
        rangeY=scene_dict['rangeY'],
        overlapPercent=scene_dict['overlapPercent']
    )
    scene.shotSequence = [Shot.from_dict(shot_dict) for shot_dict in scene_dict['shotSequence']]
    return scene