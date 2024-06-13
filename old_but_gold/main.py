#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor,GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.iodevices import I2CDevice
from pybricks.tools import wait

import connection
import threading

class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def put(self, item):
        self.items.append(item)

    def get(self):
        while self.is_empty():
            continue
        return self.items.pop(0)






ev3 = EV3Brick()

motor_left = Motor(Port.A, Direction.COUNTERCLOCKWISE)
motor_right = Motor(Port.B, Direction.COUNTERCLOCKWISE)
gyro = GyroSensor(Port.S4)
#motor1 = Motor(Port.B)
#motor2 = Motor(Port.A)
#gyro = GyroSensor(Port.S4)

axle_track = 122
wheel_diameter = 45  # Rettet stavefeil fra "wheel_diamete" til "wheel_diameter"
drive_base = DriveBase(motor_left, motor_right, wheel_diameter, axle_track)

server_socket = connection.create_server_socket(5000)
client_socket = connection.accept_connection(server_socket)

command_queue = Queue()

def robot_straight(speed):
    while command_queue.is_empty():
        correction = (0-gyro.angle())*3
        drive_base.drive(speed, correction)

def robot_turn(angle):
    drive_base.drive(0, angle)

def robot_stop():
    drive_base.stop()
    motor_left.brake()
    motor_right.brake()

# def msg_send(msg):
#    client_socket.send(msg.encode())

def execution_thread():
    while True:
        command = command_queue.get()
        print("execution_thread: ",command)
        execute_command(command)

def execute_command(command):
    if command == 'start':
        robot_straight(150)
    elif command == 'stop':
        robot_stop()
        gyro.reset_angle(0)
    elif command == 'turn':
        print(gyro.angle())
        robot_turn(360)
        print(gyro.angle())
    elif command == 'status':
        print(gyro.angle())
    elif command == 'reset':
        gyro.reset_angle(0)
    elif command == 'test':
        drive_base.drive(150, 0)


exec_thread = threading.Thread(target=execution_thread)

exec_thread.start()

try:
    gyro.reset_angle(0)
    while True:
        command = client_socket.recv(1024).decode()
        print(command)
        command_queue.put(command)
        if command == "exit":
            break
    exec_thread.join()

except:
    print("Something went wrong when writing to the file")

finally:
    client_socket.close()
    server_socket.close()
