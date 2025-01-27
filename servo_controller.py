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

        self.horizontal_servo.start(90)
        self.vertical_servo.start(90)

        self.current_horizontal_angle = [90]
        self.current_vertical_angle = [90]

    def set_servo_angle(self, servo, angle, current_angle):
        step = 1 if angle > current_angle else -1
        for i in range(current_angle, angle, step):
            duty_cycle = 2 + (i / 18)
            servo.ChangeDutyCycle(duty_cycle)
            time.sleep(0.02)  # Adjust the delay for smoother movement
        servo.ChangeDutyCycle(0)
        return angle

    def threaded_set_servo_angle(self, servo, angle, current_angle, angle_holder):
        angle_holder[0] = self.set_servo_angle(servo, angle, current_angle)

    def move_servos(self, horizontal_target_angle, vertical_target_angle):
        horizontal_thread = threading.Thread(target=self.threaded_set_servo_angle, args=(self.horizontal_servo, horizontal_target_angle, self.current_horizontal_angle[0], self.current_horizontal_angle))
        vertical_thread = threading.Thread(target=self.threaded_set_servo_angle, args=(self.vertical_servo, vertical_target_angle, self.current_vertical_angle[0], self.current_vertical_angle))
        horizontal_thread.start()
        vertical_thread.start()
        horizontal_thread.join()
        vertical_thread.join()

    def cleanup(self):
        self.horizontal_servo.stop()
        self.vertical_servo.stop()
