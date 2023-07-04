import cv2
import numpy as np
import time
from picamera2 import PiCamera2
from picamera2.array import PiRGBArray

def long_exposure():
    # Set up our PiCamera
    camera = PiCamera2()
    camera.resolution = (640, 480)  # You may change this
    camera.framerate = 24  # Set the framerate at 24 fps
    raw_capture = PiRGBArray(camera, size=(640, 480))  # You may change this

    # Allow camera to warmup
    time.sleep(0.1)

    # Setup our variables for stacking
    stack_frac = 1.0 / (camera.framerate * 3)  # Scaling factor
    stack_img = np.zeros((480, 640, 3), dtype=np.float)  # Initial black image, change size if needed
    
    # Capture continuously for 3 seconds
    end_time = time.time() + 3
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        # Add this frame to our stack
        img = frame.array
        stack_img += stack_frac * img

        # Clear the stream in preparation for the next frame
        raw_capture.truncate(0)

        # If it has been 3 seconds, break
        if time.time() > end_time:
            break

    # Normalize stack image to 8-bit (0-255)
    stack_img = cv2.normalize(stack_img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

    # Write out our stacked image to a file
    cv2.imwrite("stacked.jpg", stack_img)

long_exposure()
