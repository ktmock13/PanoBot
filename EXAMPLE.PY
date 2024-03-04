import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time

#test comment
################################
# RPi and Motor Pre-allocations
################################
#
#define GPIO pins
direction= 19 # Direction (DIR) GPIO Pin
step = 26 # Step GPIO Pin
EN_pin = 24 # enable pin (LOW to enable)

# Declare a instance of class pass GPIO pins numbers and the motor type
xmotor = RpiMotorLib.A4988Nema(4, 17, (14,15,18), "A4988")
ymotor = RpiMotorLib.A4988Nema(27, 22, (14,15,18), "A4988")

GPIO.setup(EN_pin,GPIO.OUT) # set enable pin as output

###########################
# Actual motor control
###########################
#

GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.output(24, 0)
dir_array = [False,True]
GPIO.output(EN_pin,GPIO.LOW) # pull enable to low to enable motor
for ii in range(8):
    xmotor.motor_go(dir_array[ii%1], # False=Clockwise, True=Counterclockwise
                         "1/16" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                         200, # number of steps
                         .0005, # step delay [sec]
                         True, # True = print verbose output 
                         .05) # initial delay [sec]
    ymotor.motor_go(dir_array[ii%1], # False=Clockwise, True=Counterclockwise
                         "1/16" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                         200, # number of steps
                         .0005, # step delay [sec]
                         True, # True = print verbose output 
                         .05) # initial delay [sec]
    
    GPIO.output(23, 0)
    time.sleep(.25)
    GPIO.output(23, 1)
    time.sleep(.1);

GPIO.output(24, 1)


# user inputs
camera_fov_degree = 10 # to be used to calculate moves, gather from analog input via test moves
camera_aspect_ratio = 1; #1=square, 0.5625=9:16portrait, etc
overlap_percent = 25 # higher value mean more photos, but better chance of stitching success

# calculated values
camera_fov_x_degree = 'tbd' # 
camera_fov_y_degree = 'tbd'
moves = []