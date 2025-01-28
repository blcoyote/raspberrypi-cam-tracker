import RPi.GPIO as GPIO
import time
import threading
from servo import SingleServo


class ServoController:
    def __init__(self, horizontal_pin, vertical_pin):
        self.horizontal_servo = SingleServo(horizontal_pin)
        self.vertical_servo = SingleServo(vertical_pin)

    def move_servos(self, horizontal_target_angle, vertical_target_angle):
        horizontal_thread = self.horizontal_servo.threaded_set_servo_angle(horizontal_target_angle)
        vertical_thread = self.vertical_servo.threaded_set_servo_angle(vertical_target_angle)
        horizontal_thread.join()
        vertical_thread.join()

    def get_horizontal_angle(self):
        return self.horizontal_servo.get_current_angle()

    def get_vertical_angle(self):
        return self.vertical_servo.get_current_angle()

    def cleanup(self):
        self.horizontal_servo.cleanup()
        self.vertical_servo.cleanup()
