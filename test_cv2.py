import cv2
from picamera2 import Picamera2, Preview
import time


picam2 = Picamera2()
camera_config = picam2.configure(
    picam2.create_preview_configuration(main={"format": "XRGB8888", "size": (640, 480)})
)
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
cv2.startWindowThread()
picam2.start()
time.sleep(2.0)

try:
    while True:
        frame = picam2.capture_array()
        color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow("Facial Recognition is Running", color)

    # Release the capture and close windows

except KeyboardInterrupt:
    pass
picam2.stop()
cv2.destroyAllWindows()