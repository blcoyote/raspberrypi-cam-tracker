import RPi.GPIO as GPIO
import time
import threading


class ServoController:
    def __init__(self, horizontal_pin, vertical_pin):
        self.horizontal_pin = horizontal_pin
        self.vertical_pin = vertical_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.horizontal_pin, GPIO.OUT)
        GPIO.setup(self.vertical_pin, GPIO.OUT)

        self.horizontal_servo = GPIO.PWM(self.horizontal_pin, 50)  # 50Hz frequency
        self.vertical_servo = GPIO.PWM(self.vertical_pin, 50)  # 50Hz frequency

        self.current_horizontal_angle = 90
        self.current_vertical_angle = 90
        self.horizontal_servo.start(2.5 + (self.current_horizontal_angle / 18.0))
        self.vertical_servo.start(2.5 + (self.current_vertical_angle / 18.0))

    def set_servo_angle(self, servo, target_angle, current_angle):
        step = 1 if target_angle > current_angle else -1
        for i in range(current_angle, target_angle, step):
            duty_cycle = 2.5 + (i / 18.0)
            servo.ChangeDutyCycle(duty_cycle)
            time.sleep(0.02)
        servo.ChangeDutyCycle(0)
        return target_angle

    def threaded_set_servo_angle(self, servo, target_angle, angle_variable):
        angle_variable = self.set_servo_angle(servo, target_angle, angle_variable)

    def move_servos(self, horizontal_target_angle, vertical_target_angle):
        horizontal_thread = threading.Thread(
            target=self.threaded_set_servo_angle,
            args=(
                self.horizontal_servo,
                horizontal_target_angle,
                self.current_horizontal_angle,
            ),
        )
        vertical_thread = threading.Thread(
            target=self.threaded_set_servo_angle,
            args=(
                self.vertical_servo,
                vertical_target_angle,
                self.current_vertical_angle,
            ),
        )
        horizontal_thread.start()
        vertical_thread.start()
        horizontal_thread.join()
        vertical_thread.join()

        self.current_horizontal_angle = horizontal_target_angle
        self.current_vertical_angle = vertical_target_angle

    def get_horizontal_angle(self):
        return self.current_horizontal_angle

    def get_vertical_angle(self):
        return self.current_vertical_angle

    def cleanup(self):
        self.horizontal_servo.stop()
        self.vertical_servo.stop()
        GPIO.cleanup()
