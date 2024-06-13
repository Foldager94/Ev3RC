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

from ev3_controller import Ev3Controller
from Command import Command
import connection

# Initialize the EV3 brick
ev3 = EV3Brick()

left_motor_port = Port.C
right_motor_port = Port.D
wheel_diameter = 55
axle_track = 200
gyro_port = Port.S1

robot = Ev3Controller(left_motor_port, right_motor_port, wheel_diameter, axle_track, gyro_port)

server_socket = connection.create_server_socket(5001)
client_socket = connection.accept_connection(server_socket)

def parse_command_str(command: str):
    split_command_array = command.split()
    suck = int(split_command_array[0])
    speed = int(split_command_array[1])
    angle = float(split_command_array[2])
    return Command(speed, angle)



try:
    while True:
        command_str = client_socket.recv(1024).decode()
        command = parse_command_str(command_str)
        if command.command_type() == "Unknow command":
            break
        robot.queue_put(command)




except Exception as e:
    print("Something went wrong when writing")
    print(e)
finally:
    robot.stop_controller()
    client_socket.close()
    server_socket.close()
