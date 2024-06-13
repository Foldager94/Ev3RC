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

import connection

# Initialize the EV3 brick
ev3 = EV3Brick()

arduino = UARTDevice( Port.S1, 9600 )

server_socket = connection.create_server_socket(5000)
client_socket = connection.accept_connection(server_socket)


try:
    while True:
        command = client_socket.recv(1024).decode()
        if command == "f":
            print("Starts sucking")
            arduino.write(b'f')
        elif command == "F":
            arduino.write(b'F')
            print("Stop sucking")
        elif command == "t":
            arduino.write(b't')
            print("Stop sucking")
        if command == "exit":
            break

except:
    print("Something went wrong when writing to the file")

finally:
    client_socket.close()
    server_socket.close()
