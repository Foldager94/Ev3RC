#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import (Motor,GyroSensor)
from pybricks.robotics import DriveBase
import _thread
from Queue import Queue
from pybricks.parameters import Port, Direction
from time import sleep


class Ev3Controller:
    def __init__(self, left_motor_port, right_motor_port):
        self.left_motor = Motor(left_motor_port)
        self.right_motor = Motor(right_motor_port)
        self.queue = Queue()
        self.running = True
        _thread.start_new_thread(self.controller, ())

    def executer(self, command):
        if command.command_type() == "straight":
            self.robot_straight(command.speed())
        elif command.command_type() == "stop":
            self.robot_stop()
        else:
            print("Command not found")


    def controller(self):
        while self.running:
            command = self.queue.get()
            self.executer(command)

    def robot_run(self, lm_speed, rm_speed):
        self.left_motor.run(lm_speed)
        self.right_motor.run(rm_speed)

    def robot_stop(self):
        self.left_motor.stop()
        self.right_motor.stop()

    def robot_turn(self, lm_speed, rm_speed):
        self.left_motor.run(lm_speed)
        self.right_motor.run(rm_speed)

    def queue_put(self, value):
        self.queue.put(value)

    def stop_controller(self):
        self.running = False
        self.queue.put(None)
