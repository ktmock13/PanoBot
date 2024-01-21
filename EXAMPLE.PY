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
mymotortest = RpiMotorLib.A4988Nema(direction, step, (5,6,13), "DRV8825")
GPIO.setup(EN_pin,GPIO.OUT) # set enable pin as output

###########################
# Actual motor control
###########################
#
dir_array = [False,True]
GPIO.output(EN_pin,GPIO.LOW) # pull enable to low to enable motor
for ii in range(10):
    mymotortest.motor_go(dir_array[ii%2], # False=Clockwise, True=Counterclockwise
                         "1/4" , # Step type (Full,Half,1/4,1/8,1/16,1/32)
                         200, # number of steps
                         .0005, # step delay [sec]
                         False, # True = print verbose output 
                         .05) # initial delay [sec]
    time.sleep(1)

GPIO.cleanup() # clear GPIO allocations after run


# user inputs
camera_fov_degree = 10 # to be used to calculate moves, gather from analog input via test moves
camera_aspect_ratio = 1; #1=square, 0.5625=9:16portrait, etc
overlap_percent = 25 # higher value mean more photos, but better chance of stitching success

# calculated values
camera_fov_x_degree = 'tbd' # 
camera_fov_y_degree = 'tbd'
moves = []