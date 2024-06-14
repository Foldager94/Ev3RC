#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.iodevices import I2CDevice, UARTDevice
from pybricks.tools import wait

#from ev3_controller import Ev3Controller
import connection

# Initialize the EV3 brick
ev3 = EV3Brick()

left_motor = Motor(Port.C)
right_motor = Motor(Port.D)


server_socket = connection.create_server_socket(5001)
client_socket = connection.accept_connection(server_socket)

def split_command(command: str):
    split_command_array = command.split()
    lm_speed = float(split_command_array[0])
    rm_speed = float(split_command_array[1])
    suck = int(split_command_array[2])
    print(lm_speed, rm_speed, suck)
    return lm_speed, rm_speed, suck

def robot_run(lm_speed, rm_speed):
    speed = 1050
    left_motor.run(speed*lm_speed)
    right_motor.run(speed*rm_speed)

def robot_stop():
    left_motor.stop()
    right_motor.stop()
try:
    while True:
        data = client_socket.recv(1024).decode()
        if data == "exit":
            break
        lm_speed, rm_speed, suck = split_command(data)
        if lm_speed != 0 or rm_speed != 0:
            robot_run(lm_speed, rm_speed)
        elif lm_speed == 0 and rm_speed == 0:
            robot_stop()




except Exception as e:
    print("Something went wrong when writing")
    print(e)
finally:
    client_socket.close()
    server_socket.close()
