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

left_motor = Motor(Port.A)
right_motor = Motor(Port.B)

arduino = UARTDevice( Port.S4, 9600 )

# Opens server on port 5000 by default
server_socket = connection.create_server_socket()
client_socket = connection.accept_connection(server_socket)

def split_command(command: str):
    split_command_array = command.split()
    try:
        lm_speed = float(split_command_array[0])
        rm_speed = float(split_command_array[1])
        suck = int(split_command_array[2])
        latch = int(split_command_array[3])
        print(lm_speed, rm_speed, suck)
        return lm_speed, rm_speed, suck, latch
    except Exception as e:
        print("Error in split_command:", e)

def robot_run(lm_speed, rm_speed):
    max_speed = 800
    left_motor.run(max_speed*lm_speed)
    right_motor.run(max_speed*rm_speed)

def robot_stop():
    left_motor.stop()
    right_motor.stop()

def fan_start():
    try:
        arduino.write(b'f')
    except Exception as e:
        print("fan_start",e)

def fan_stop():
    try:
        arduino.write(b'F')
    except Exception as e:
        print("fan_stop",e)

def latch_open():
    try:
        arduino.write(b'l')
    except Exception as e:
        print("latch_open",e)

def latch_close():
    try:
        arduino.write(b'L')
    except Exception as e:
        print("latch_close",e)

def fan_test():
    try:
        arduino.write(b't')
    except Exception as e:
        print("fan_start",e)

try:
    is_sucking = 0
    is_latch_open = 0
    while True:
        data = client_socket.recv(1024).decode()
        if data == "exit":
            break
        if data == "status":
            print(left_motor.control.limits())
            print(right_motor.control.limits())
            continue
        lm_speed, rm_speed, suck, latch = split_command(data)
        if lm_speed != 0 or rm_speed != 0:
            #robot_run(lm_speed, rm_speed)
            print("Robt_run:\nLeft motor speed:",lm_speed,"\nRight motor speed:",rm_speed)
        elif lm_speed == 0 and rm_speed == 0:
            #robot_stop()
            print("Robot_stop")
        if is_sucking != suck:
            is_sucking = suck
            if suck == 1:
                fan_start()
                print("Fan started")
            elif suck == 0:
                fan_stop()
                print("Fan stopped")
        if is_latch_open != latch:
            is_latch_open = latch
            if latch == 1:
                latch_open()
                print("Latch open")
            elif latch == 0:
                latch_close()
                print("Latch close")



except Exception as e:
    print("Something went wrong when writing")
    print(e)
finally:
    print("Shutting down")
    client_socket.close()
    server_socket.close()
    print("client and server sockets closed")
