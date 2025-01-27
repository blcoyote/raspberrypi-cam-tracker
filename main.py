from servo_controller import ServoController
import time
import cv2
from picamera2 import Picamera2, Preview

picam2 = Picamera2()
camera_config = picam2.configure(
    picam2.create_preview_configuration(main={"format": "XRGB8888", "size": (640, 480)})
)
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
cv2.startWindowThread()
picam2.start()
time.sleep(2.0)


servo_controller = ServoController(horizontal_pin=23, vertical_pin=22)


# Global variables for desired angles
desired_horizontal_angle = 90
desired_vertical_angle = 90


def update_angles():
    global desired_horizontal_angle, desired_vertical_angle

    if (
        servo_controller.get_horizontal_angle() != desired_horizontal_angle
        or servo_controller.get_vertical_angle() != desired_vertical_angle
    ):
        servo_controller.move_servos(desired_horizontal_angle, desired_horizontal_angle)


try:
    while True:
        frame = picam2.capture_array()
        color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Example: Update desired angles
        desired_horizontal_angle = 90
        desired_vertical_angle = 45
        update_angles()

        cv2.imshow("Facial Recognition is Running", color)

    # Release the capture and close windows

except KeyboardInterrupt:
    pass
picam2.stop()
cv2.destroyAllWindows()
