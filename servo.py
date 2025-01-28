import time
import threading
import RPi.GPIO as GPIO

class SingleServo:
    def __init__(self, pin):
        self.pin = pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

        self.servo = GPIO.PWM(self.pin, 50)  # 50Hz frequency

        self.current_angle = 90
        self.servo.start(2.5 + (self.current_angle / 18.0))

    def set_servo_angle(self, target_angle):
        step = 1 if target_angle > self.current_angle else -1
        for i in range(self.current_angle, target_angle, step):
            duty_cycle = 2.5 + (i / 18.0)
            self.servo.ChangeDutyCycle(duty_cycle)
            time.sleep(0.02)
        self.current_angle = target_angle

    def threaded_set_servo_angle(self, target_angle):
        thread = threading.Thread(target=self.set_servo_angle, args=(target_angle,))
        thread.start()
        return thread
    
    def get_current_angle(self):
        return self.current_angle
    
    def cleanup(self):
        self.servo.stop()
        GPIO.cleanup()

