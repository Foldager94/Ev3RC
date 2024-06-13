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

drive_base = DriveBase(left_motor, right_motor, 55, 200)

server_socket = connection.create_server_socket(5000)
client_socket = connection.accept_connection(server_socket)

def split_command(command: str):
    split_command_array = command.split()
    suck = int(split_command_array[0])
    speed = int(split_command_array[1])
    angle = float(split_command_array[2])
    print(suck, speed, angle)
    if speed == 0 and angle == 0.0:
        print("command: stop")
        return ("stop", speed, angle)
    elif speed != 0 and angle == 0.0:
        print("command: straight")
        return ("straight", speed)
    elif speed == 0 and angle != 0:
        print("command: turn")
        return ("turn", angle)
    elif speed != 0 and angle != 0:
        print("command: strafe")
        return ("strafe", speed, angle)
    return ("Unknow command")



try:
    while True:
        data = client_socket.recv(1024).decode()
        if data == "exit":
            break
        command = split_command(data)
        print("recived:",command)
        if command[0] == "straight":
            print("straight")
            drive_base.drive(command[1], 0)
        elif command[0] == "strafe":
            print("strafe")
            drive_base.drive(command[1], command[2])
        elif command[0] == "stop":
            print("stop")
            drive_base.stop()
            left_motor.brake()
            right_motor.brake()
        elif command[0] == "turn":
            drive_base.drive(command[1])


except Exception as e:
    print("Something went wrong when writing")
    print(e)
finally:
    client_socket.close()
    server_socket.close()
