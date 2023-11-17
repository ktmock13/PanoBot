import math
import time

class Shot:
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
    def __str__(self):
        return f"Shot at ({self.x}, {self.y}), Height: {self.height}, Width: {self.width}"

class Camera:
    def __init__(self, fovDegrees, aspectRatio, meta = {'name': 'unnamed camera', 'shotSizeMB': '0'}, display):
        self.fovDegrees = fovDegrees  # assumed to be widest dimension of rectangle
        self.aspectRatio = aspectRatio
        self.isLandscape = aspectRatio >= 1
        self.meta = meta
        # calculate shotHeight and shotWidth based on fov and aspect

    def printInfo(self):
        print('\n\nCamera Info - User Input')
        print(f'- Name: {self.meta["name"]}')
        print(f'- Degrees FOV: {self.fovDegrees}')
        print(f'- Aspect Ratio: {self.aspectRatio} ({ "square " if self.aspectRatio == 1 else ("landscape" if self.isLandscape else "portrait")})')
        print(f'- Size MB: {self.meta["shotSizeMB"]}')

    def getHorizontalFov(self):
        # if this is a landscape photo, the self.fovDegrees value is the horizontal fov
        return self.fovDegrees if self.isLandscape else self.fovDegrees * self.aspectRatio

    def getVerticalFov(self):
        # if this is a portrait photo, the self.fovDegrees value is the vertical fov
        return self.fovDegrees if not self.isLandscape else self.fovDegrees * (1 / self.aspectRatio)

class Scene:
    def __init__(self, cameraFOV, cameraAspect, rangeX, rangeY, overlapPercent, display):
        self.camera = Camera(cameraFOV, cameraAspect)
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

    def printInfo(self):
        self.camera.printInfo()
        print('\n\nScene Info')
        print(f'- Pano FOV (user input): {self.rangeX}x{self.rangeY}')
        print(f'- Pano Grid: {self.sceneDimensions}')
        print(f'- Number of shots: {len(self.shotSequence)}')
        print(f'- Total MB: {len(self.shotSequence) * int(self.camera.meta["shotSizeMB"])}')
        print('\n\n')

    def runScene(self, delay):
        def timeout(ms):
            time.sleep(ms / 1000)
        if self.shotSequence:
            for shot in self.shotSequence:
                # code to move, use current shot
                print(shot)
                timeout(delay / 2)
                # code to take photo
                print('capture... ')
                timeout(delay / 2)