#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import (Motor,GyroSensor)
from pybricks.robotics import DriveBase
import _thread
from Queue import Queue
from pybricks.parameters import Port, Direction
from time import sleep


class Ev3Controller:
    def __init__(self, left_motor_port, right_motor_port, wheel_diameter: int, axle_track: int, gyro_sensor_port):
        self.left_motor = Motor(left_motor_port)
        self.right_motor = Motor(right_motor_port)
        self.wheel_diameter = wheel_diameter
        self.axle_track = axle_track
        self.drive_base = DriveBase(self.left_motor, self.right_motor, self.wheel_diameter, self.axle_track)
        self.gyro = GyroSensor(gyro_sensor_port)
        self.queue = Queue()
        self.running = True
        _thread.start_new_thread(self.controller, ())

    def executer(self, command):
        if command.command_type() == "straight":
            self.robot_straight(command.speed())
        elif command.command_type() == "strafe":
            self.robot_strafe(command.speed(), command.angle())
        elif command.command_type() == "stop":
            self.robot_stop()
        elif command.command_type() == "turn":
            self.robot_turn(command.angle())
        elif command.command_type() == "calibrate":
            print("not implementet")
        elif command.command_type() == "test":
            self.robot_debug()
        else:
            print("Command not found")


    def controller(self):
        while self.running:
            command = self.queue.get()
            self.executer(command)

    def robot_straight(self, speed):
        current_correction = 0
        start_angle = self.gyro.angle()
        print("start angle:",current_correction)
        self.drive_base.drive(speed, 0)
        while self.queue.is_empty():
            sleep(1)
            angle = self.gyro.angle()
            correction = (start_angle-angle)*3
            print("current angle:",angle, "| current correction",correction)
            if -3 > correction < 3 and correction != current_correction:
                self.drive_base.drive(speed, correction)
                current_correction = current_correction

    def robot_strafe(self, speed, angle):
        self.drive_base.drive(speed, angle)

    def robot_turn(self, angle):
        self.robot_stop()
        self.drive_base.turn(angle)

    def robot_stop(self):
        self.drive_base.stop()
        self.left_motor.brake()
        self.right_motor.brake()

    def robot_debug(self):
        self.left_motor.reset_angle(0)
        self.gyro.reset_angle(0)
        self.left_motor.run_time(100, 2000)
        lm_angle = self.left_motor.angle()
        print("Left Motor Angle:", lm_angle, "| Gyro angle:", self.gyro.angle())
        self.right_motor.reset_angle(0)
        self.right_motor.run_time(100, 2000)
        rm_angle = self.right_motor.angle()
        print("Left Motor Angle:", lm_angle, "| Gyro angle:", self.gyro.angle())

    def queue_put(self, value):
        self.queue.put(value)

    def stop_controller(self):
        self.running = False
        self.queue.put(None)
