# PanoBot - AI Developer Guide

## Project Overview

PanoBot is a Raspberry Pi-based panoramic photography automation system that controls stepper motors to position a camera for capturing high-resolution panoramic images. It uses a web-based scene simulator and an on-device menu interface to calculate optimal shot sequences, then automatically captures photos with precise motor positioning.

## Architecture Overview

### Core Components

```
┌─────────────────────────────────────────────────────────┐
│                    PANOBOT SYSTEM                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐   │
│  │   Menu       │  │   Display    │  │  Camera    │   │
│  │  (GPIO UI)   │  │  (OLED/LCD)  │  │  (Shutter) │   │
│  └──────┬───────┘  └──────┬───────┘  └────┬───────┘   │
│         │                 │               │            │
│         └─────────────┬───┴───────────────┘            │
│                       │                                 │
│              ┌────────▼────────┐                        │
│              │    Scene        │                        │
│              │   (Planning)    │                        │
│              └────────┬────────┘                        │
│                       │                                 │
│              ┌────────▼────────┐                        │
│              │    Robot        │                        │
│              │  (Motor Control)│                        │
│              └─────────────────┘                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Key Modules

**1. Robot (`robot.py`)**
- Controls two stepper motors (X and Y axes)
- Uses A4988 motor drivers with GPIO pins
- Manages motor positioning with configurable step types (Full, Half, 1/4, 1/8, 1/16, 1/32)
- Tracks current position and converts desired angles to stepper steps
- Provides `updatePosition()` and `centerToHome()` methods

**2. Camera (`camera.py`)**
- Manages camera parameters (FOV, aspect ratio)
- Calculates horizontal and vertical fields of view based on orientation
- Controls shutter relay via GPIO pin 23
- Provides `capture()` method to trigger photography

**3. Scene (`scene.py`)**
- Core planning algorithm that calculates shot sequence
- Uses camera FOV and desired panorama coverage (rangeX, rangeY)
- Calculates optimal overlap percentage between shots
- Generates ordered shot sequence (sweeping L-to-R, R-to-L pattern)
- Orchestrates the actual capture process: positioning → delay → capture
- Manages execution state and supports cancellation

**4. Display (`display.py`)**
- Controls OLED/LCD display (128x32 pixels)
- Provides logging interface for progress feedback
- Shows loading bars during capture
- Manages menu and log screen rendering
- Uses I2C interface via Adafruit SSD1306 driver

**5. Menu (`menu.py`)**
- Interactive menu system on physical OLED display
- Three GPIO buttons: UP (16), SELECT (20), DOWN (21)
- Edit mode allows value adjustment with increment/decrement
- Manages scene execution in separate thread
- Settings stored in `menu_items` list

**6. Hardware Control (`index.py`, `exit.py`, `shutter.py`)**
- `index.py`: Main entry point, initializes GPIO and starts menu
- `exit.py`: GPIO cleanup and relay deactivation
- `shutter.py`: Alternative Bluetooth-controlled shutter trigger

### Web Simulation Layer

**Dual JavaScript/Python Implementation:**
- `index.html` + embedded JavaScript: Browser-based scene simulator
- `scene.js`: Standalone scene algorithm (for testing/visualization)
- `menu.html`: Browser simulation of the physical menu interface
- Python equivalents in `scene.py` and `robot.py` for hardware execution

Both implementations use identical algorithms for compatibility.

## Development Setup

### Dependencies (Hardware-specific)
```
RPi.GPIO          - GPIO pin control
RpiMotorLib        - Stepper motor library (A4988)
PIL (Pillow)       - Image manipulation for display
adafruit_ssd1306   - OLED display driver
board              - Circuit Python board definitions
busio              - I2C interface library
evdev              - Input event handling
pybluez            - Bluetooth connectivity
```

### Install on Raspberry Pi
```bash
# Install system packages
sudo apt-get install python3-pip python3-dev

# Install Python dependencies (note: most are RPi-specific)
pip3 install RPi.GPIO
pip3 install RpiMotorLib
pip3 install Pillow
pip3 install adafruit-circuitpython-ssd1306
pip3 install pybluez
pip3 install evdev
```

## Common Commands

### Running on Raspberry Pi

**Start the main menu interface:**
```bash
python3 index.py
```

This initializes GPIO, sets up the menu on the OLED display, and waits for button input.

**Test mode (DEBUG):**
```bash
# Edit constants.py and set DEBUG = True
# This prevents actual motor movement and GPIO commands
python3 index.py
```

### Web Simulation (Local Development)

**Scene Simulator (calculate shot positions):**
- Open `index.html` in a browser
- Configure camera specs and desired panorama size
- Click "Generate Scene" to visualize shot positions
- Export stitching metadata as XML (Papywizard format)

**Menu Simulator (test interface):**
- Open `menu.html` in a browser
- Use arrow keys to navigate, Enter to select/edit

### Manual Motor Testing

```bash
# Test motor initialization
python3 -c "from robot import Robot; r = Robot(6)"

# Test camera capture
python3 -c "from camera import Camera; c = Camera(15.5, 0.75); c.capture()"
```

## Configuration

### Important Constants

**In `constants.py`:**
- `DEBUG = False` - Set to `True` to disable GPIO/motor commands for testing

**In `robot.py`:**
- GPIO pins for motors:
  - X-axis: DIR=4, STEP=17
  - Y-axis: DIR=27, STEP=22
  - Settings: (14, 15, 18)
- Step types and their degree increments:
  - Full: 1.8°
  - Half: 0.9°
  - 1/16: 0.1125° (default precision)
  - 1/32: 0.05625° (highest precision)

**In `camera.py`:**
- Shutter relay: GPIO pin 23

**In `scene.py`:**
- Stepper relay: GPIO pin 24

**In `menu.py`:**
- Button pins: UP=16, SELECT=20, DOWN=21
- Display: I2C SSD1306 (128x32 pixels)

### Menu Items (Adjustable Parameters)

```python
[
  {"id": "cameraFOV", "value": 15.5, "increment": 0.5},
  {"id": "cameraAspectRatio", "value": 0.75, "increment": 0.05},
  {"id": "overlapPercent", "value": 0.15, "increment": 0.05},
  {"id": "rangeX", "value": 100, "increment": 5},  # Desired X FOV in degrees
  {"id": "rangeY", "value": 50, "increment": 5},   # Desired Y FOV in degrees
  {"id": "focusDelay", "value": 1000, "increment": 100},  # ms
  {"id": "exposureDelay", "value": 1000, "increment": 100},  # ms
  {"id": "robotSpeed", "value": 6, "increment": 1},  # Motor speed (1-11)
]
```

## Key Algorithms

### Shot Sequence Generation

1. Calculate individual shot FOV based on camera specs
2. Determine spacing between shots: `spacing = fov * (1 - overlapPercent)`
3. Calculate required grid dimensions:
   - `sceneDimensionX = ceil((rangeX - overlapAmount) / xSpacing)`
   - `sceneDimensionY = ceil((rangeY - overlapAmount) / ySpacing)`
4. Generate shots in boustrophedon (snake) pattern:
   - Even rows: left-to-right
   - Odd rows: right-to-left
5. Output: Ordered list of (x, y) positions for each shot

### Motor Control

1. Calculate angle difference: `desiredAngle - currentPosition`
2. Convert to steps: `steps = angle / stepDegrees[stepType]`
3. Execute motor movement with:
   - Direction bit (clockwise/counterclockwise)
   - Step count
   - Delay between steps (affects speed)
4. Update position: `currentPosition += actualAngleMoved`

### Scene Execution Flow

```
1. Create Robot instance (initializes motor drivers)
2. Activate stepper relay (GPIO 24 LOW)
3. Center motors to home position
4. For each shot in sequence:
   a. Update motor positions
   b. Wait for focus delay
   c. Capture photo (GPIO 23 pulse)
   d. Update progress bar on display
   e. Wait for exposure delay
5. Reverse shot sequence (return sweep)
6. Repeat steps 4 (backward capture)
7. Deactivate stepper relay (GPIO 24 HIGH)
```

## File Structure

```
PanoBot/
├── index.py              # Entry point, GPIO initialization
├── menu.py              # Menu UI and button handling
├── scene.py             # Scene planning and execution
├── robot.py             # Motor control (X, Y axes)
├── camera.py            # Camera shutter control
├── display.py           # OLED display interface
├── shutter.py           # Bluetooth shutter alternative
├── exit.py              # GPIO cleanup
├── constants.py         # Global DEBUG flag
├── index.html           # Scene simulator (browser)
├── menu.html            # Menu simulator (browser)
├── scene.js             # Standalone scene algorithm
├── CLAUDE.md            # This file
└── logfile.log          # Runtime logs
```

## Data Flow Examples

### Scenario 1: Simulating a 120° x 60° panorama with iPhone 5x (15.5°, 0.75 AR)

**Input Parameters:**
- Camera FOV: 15.5°
- Aspect Ratio: 0.75 (portrait)
- Desired Coverage: 120° x 60°
- Overlap: 15%

**Calculations:**
- Horizontal FOV: 15.5° × 0.75 = 11.625°
- Vertical FOV: 15.5°
- X Spacing: 11.625° × (1 - 0.15) = 9.88°
- Y Spacing: 15.5° × (1 - 0.15) = 13.175°
- X Shots: ceil((120 - 1.75) / 9.88) = 12
- Y Shots: ceil((60 - 1.825) / 13.175) = 5
- **Total: 60 shots in a 12×5 grid**

**Shot Sequence:**
```
Row 0 (LTR):  (0,0) → (9.88,0) → (19.76,0) → ... → (108.68,0)
Row 1 (RTL):  (108.68,13.175) → ... → (0,13.175)
Row 2 (LTR):  (0,26.35) → ... → (108.68,26.35)
... and so on
```

### Scenario 2: Executing Scene on Hardware

1. User navigates menu, selects "START"
2. Scene created with current parameters
3. Robot initialized (motors powered via GPIO 24 = LOW)
4. Motors centered to home (0,0)
5. For each of 60 shots:
   - Move to position
   - Sleep 1000ms (focus)
   - Trigger shutter (GPIO 23 pulse)
   - Show progress on OLED
   - Sleep 1000ms (exposure)
6. Reverse order, repeat
7. Motors deactivated (GPIO 24 = HIGH)

## Hardware Integration Notes

### GPIO Pin Mapping
```
Motor X: DIR=4, STEP=17
Motor Y: DIR=27, STEP=22
Motor Settings: GPIO 14, 15, 18 (mode selection)
Stepper Relay: GPIO 24
Shutter Relay: GPIO 23
Menu Buttons: UP=16, SELECT=20, DOWN=21
```

### Motor Speed Control
- Speed parameter (1-11) affects step delay
- Formula: `stepDelay = max(0.001, min(0.01, abs(speed-11) * 0.001))`
- Speed=6 → ~0.005s delay (optimal)
- Higher values = slower but more power

### Relay Logic
- **Active (motor/shutter on):** GPIO = LOW
- **Inactive (motor/shutter off):** GPIO = HIGH
- Stepper relay must be LOW during motor movement

## Testing & Debugging

### Enable Debug Mode
Edit `constants.py`:
```python
DEBUG = True
```
This prevents GPIO commands from executing, allowing testing on non-RPi systems.

### Log Output
- Check `logfile.log` for runtime events
- Menu execution logs to stdout
- Motor movements print position updates

### Common Issues

**Issue: Motors don't move**
- Check `constants.DEBUG` - must be False on RPi
- Verify relay GPIO pins and activation (should be LOW for active)
- Check GPIO.setmode() called before motor operations

**Issue: Menu doesn't respond**
- Verify button GPIO pins (16, 20, 21)
- Check I2C connection to OLED display
- Review button debounce time (150ms)

**Issue: Shot sequence incorrect**
- Verify camera FOV and aspect ratio parameters
- Check overlap percentage (0-1 range)
- Confirm rangeX, rangeY values in degrees

## Export and Integration

### Papywizard XML Export
The scene simulator can export shot coordinates in Papywizard format (XML):
```xml
<?xml version="1.0" encoding="utf-8"?>
<papywizard>
  <shoot>
    <pict bracket="1">
      <position pitch="-30" yaw="-60"/>
    </pict>
    <\!-- More shots... -->
  </shoot>
</papywizard>
```

This can be imported into panoramic stitching software.

## Development Workflow

1. **Algorithm Testing:** Use browser simulators (index.html, menu.html)
2. **Local Testing:** Run Python with DEBUG=True (no GPIO)
3. **Hardware Testing:** Deploy to RPi, DEBUG=False
4. **Integration:** Test with actual motor hardware and camera

## Future Considerations

- Add web server for remote scene triggering
- Implement shot preview/validation
- Add exposure bracketing for HDR panoramas
- Support for multiple camera types (preset library)
- Real-time motor position feedback
- Thermal/vibration compensation
