import time
from picamera2 import Picamera2, MappedArray, Preview
import cv2

picam2 = Picamera2()
camera_config = picam2.configure(
    picam2.create_preview_configuration(main={"format": "XRGB8888", "size": (640, 480)})
)
picam2.configure(camera_config)

cv2.startWindowThread()
colour = (0, 255, 0)
origin = (0, 30)
font = cv2.FONT_HERSHEY_SIMPLEX
scale = 1
thickness = 2

def apply_timestamp(request):
  timestamp = time.strftime("%Y-%m-%d %X")
  with MappedArray(request, "main") as m:
    cv2.putText(m.array, timestamp, origin, font, scale, colour, thickness)

picam2.pre_callback = apply_timestamp
picam2.start(Preview.QTGL)

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