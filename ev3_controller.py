from pybricks.ev3devices import (Motor,GyroSensor)
from pybricks.robotics import DriveBase
import _thread
import Queue

class EV3_Controller:
    def __init__(self, left_motor_port, right_motor_port, wheel_diameter, axle_track, gyro_sensor_port):
        self.left_motor = Motor(left_motor_port)
        self.right_motor = Motor(right_motor_port)
        self.wheel_diameter = wheel_diameter
        self.axle_track = axle_track
        self.drive_base = DriveBase(self.left_motor, self.right_motor, self.wheel_diameter, self.axle_track)
        self.gyro = GyroSensor(gyro_sensor_port)
        self.queue = Queue()
        self.running = True
        _thread.start_new_thread(self.controller, ())

    def controller(self):
        while self.running:
            command = self.queue.get()
            self.executer(command)

    def executer(self, command):
        if command == "straight":
            self.fan_start()
        elif command == "stop":
            self.fan_stop()
        elif command == "turn":
            self.latch_open()
        elif command == "calibrate":
            self.latch_close()
        elif command == "test":
            self.fan_test()
        else:
            print(f"Command not found: {command}")

    def robot_straight(speed):
        while command_queue.is_empty():
            correction = (0-gyro.angle())*3
            drive_base.drive(speed, correction)

    def robot_turn(angle):
        robot_stop()
        drive_base.turn(angle)

    def robot_stop():
        drive_base.stop()
        motor_left.brake()
        motor_right.brake()

    def queue_put(self, value):
        self.queue.put(value)

    def stop_controller(self):
        self.running = False
        self.queue.put(None)