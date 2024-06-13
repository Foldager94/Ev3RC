#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.iodevices import I2CDevice
from pybricks.tools import wait


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
motor1 = Motor(Port.A, Direction.COUNTERCLOCKWISE)
motor2 = Motor(Port.B, Direction.COUNTERCLOCKWISE)
gyro = GyroSensor(Port.S4, Direction.COUNTERCLOCKWISE)


#axle_track = 166
axle_track = 147.2
wheel_diamete = 37.8
drive_base = DriveBase(motor1,motor2,wheel_diamete,axle_track)


# Write your program here.

# Define the I2C address of the Arduino
ARDUINO_ADDRESS = 0x08

# Initialize the I2C device
i2c = I2CDevice(Port.S1, ARDUINO_ADDRESS)

def read_from_arduino():
    try:
        # Read one byte from the Arduino
        data = i2c.read(1)
        print("Received data:", data)
    except Exception as e:  
        print("Failed to read from Arduino:", e)

def write_to_arduino(value):
    try:
        # Write one byte to the Arduino
        i2c.write(value)
        print("Sent data:", value)
    except Exception as e:
        print("Failed to write to Arduino:", e)

def turn(deg):
    start_angle = gyro.angle()
    print("Start Angle:", start_angle, " | Deg to turn:", deg)
    drive_base.turn(deg)
    current_angle = gyro.angle()
    print("Current Angle:", gyro.angle())
    if(start_angle+deg != current_angle):
        turn(deg-current_angle)

def calibrate_drive_base():
    global drive_base
    global axle_track
    while(True):
        gyro.reset_angle(0)
        drive_base.turn(360)
        print("Actual angle:",gyro.angle())
        off_set = 360 - gyro.angle()
        print("Off by: ",off_set)
        if(off_set == 0):
            print("Axle_track calibration done!")
            break
        if(off_set < 0):
            axle_track -= 1
        if(off_set > 0):
            axle_track += 0.4
        drive_base.stop()
        print(axle_track)
        drive_base = DriveBase(motor1,motor2,wheel_diamete,axle_track)


def calibrate_drive_base_axle_track():

    return 360 - gyro.angle()


def calibrate_drive_base_wheel_diameter():
    return
    
def drive_base_drive(speed, angle):
    drive_base.drive(speed, angle)


if __name__ == "__main__":
    ev3.speaker.set_volume(100)
    ev3.speaker.play_file("/home/robot/test/test.wav")