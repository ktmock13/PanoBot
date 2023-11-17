
const ZOOM = 10; // each pixel is represented as 1 degree, this zoom multiplier does just that
class Shot {
  constructor(x, y, height, width) {
    this.x = x;
    this.y = y;
    this.height = height;
    this.width = width;
  }
}

class Camera {
  constructor(fovDegrees, aspectRatio, meta = { name: 'unnamed camera', shotSizeMB: '0'}) {
    this.fovDegrees = fovDegrees; // assumed to be widest dimension of rectangle
    this.aspectRatio = aspectRatio;
    this.isLandscape = aspectRatio >= 1
    this.meta = meta;
    //calculate shotHeight and shotWidth based on fov and aspect
  }
  printInfo() {
    console.log(`\n\nCamera Info - User Input`)
    console.log(`- Name: ${this.meta.name}`);
    console.log(`- Degrees FOV: ${this.fovDegrees}`);
    console.log(`- Aspect Ratio: ${this.aspectRatio} (${this.aspectRatio===1?'square ': (this.isLandscape?'landscape':'portrait')})`);
    console.log(`- Size MB: ${this.meta.shotSizeMB}`);

  }
  getHorizontalFov() {
    // if this is a landscape photo, the this.fovDegrees value is the horizontal fov
    return this.isLandscape ? this.fovDegrees : this.fovDegrees * this.aspectRatio;
  }
  getVerticalFov() {
    // if this is a portrait photo, the this.fovDegrees value is the vertical fov
    return !this.isLandscape ? this.fovDegrees : this.fovDegrees * (1 / this.aspectRatio);
  }
}

class Scene {
  constructor(camera, rangeX, rangeY, overlapPercent = 0.333) {
    this.camera = camera;
    this.rangeX = rangeX; // total FOV degrees desired, ex. 100
    this.rangeY = rangeY; // total FOV degrees desired, ex. 50
    this.shotSequence = [] // will be computed below

    // FOV units between shots, considering overlap
    const xSpacing = (this.camera.getHorizontalFov() * (1 - overlapPercent))
    const ySpacing = (this.camera.getVerticalFov() * (1 - overlapPercent))

    // Amount of FOV units that the shots overlap
    const xOverlapAmount = (this.camera.getHorizontalFov() - xSpacing);
    const yOverlapAmount = (this.camera.getVerticalFov() - ySpacing);

    // Min # of photos in each dimension to cover the desired range
    let sceneDimensionX = Math.ceil((rangeX - xOverlapAmount) / xSpacing);
    let sceneDimensionY = Math.ceil((rangeY - yOverlapAmount) / ySpacing);

    this.sceneDimensions = `${sceneDimensionX}x${sceneDimensionY}`

    // All shots will be calculated from this frame of reference
    const firstShot = new Shot(0, 0, this.camera.getHorizontalFov(), this.camera.getVerticalFov())
    // Helper function to move to make new shots relative to a shot
    const createMovedShot = (shot, xDistance, yDistance) => new Shot(shot.x + xDistance, shot.y + yDistance, shot.height, shot.width)
    for (let iy = 0; iy < sceneDimensionY; iy++) {
      for (let ix = 0; ix < sceneDimensionX; ix++) {
        // compute each shot
        this.shotSequence.push(createMovedShot(firstShot, ix * xSpacing, iy * ySpacing))
      }
    }
  }
  printInfo(){
    this.camera.printInfo()
    console.log(`\n\nScene Info`)
    console.log(`- Pano FOV (user input): ${this.rangeX}x${this.rangeY}`)
    console.log(`- Pano Grid: ${this.sceneDimensions}`)
    console.log(`- Number of shots: ${this.shotSequence.length}`)
    console.log(`- Total MB: ${this.shotSequence.length*this.camera.meta.shotSizeMB}`)

    console.log(`\n\n`)
  }
  async runScene(delay) {
    function timeout(ms) {
      return new Promise(resolve => setTimeout(resolve, ms))
    }
    if (this.shotSequence.length) {
      for (let shot of this.shotSequence) {
        // code to move, use current shot 
        console.log(`moving to...  ${JSON.stringify(shot)}`)
        await timeout(delay / 2)
        // code to take photo
        console.log('capture... ')
        await timeout(delay / 2)
      }
    }
  }
}

const iPHONE_5X_PORT = new Camera(11.3, .75, {name: 'iPhone 15 Pro Max 5x lens (120MM)', shotSizeMB: '10'});

const scene = new Scene(iPHONE_5X_PORT, 120, 60, .15, "shotCanvas1");

scene.printInfo()
scene.runScene(100)

