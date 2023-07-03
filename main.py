from collections import deque
import cv2
import numpy as np
import time
from picamera import PiCamera
from picamera.array import PiRGBArray

def rolling_long_exposure():
    # Set up our PiCamera
    camera = PiCamera()
    camera.resolution = (640, 480)  # You may change this
    camera.framerate = 24  # Set the framerate at 24 fps
    raw_capture = PiRGBArray(camera, size=(640, 480))  # You may change this 

    # Allow camera to warmup
    time.sleep(0.1)

    # Setup our variables for buffer and counter
    buffer = deque(maxlen=72) # a deque only stores the latest 72 images
    frame_counter = 0

    # Capture continuously
    for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
        # Add the latest frame to the buffer and the buffer only stores the latest 72 frames 
        img = frame.array
        buffer.append(img * 1.0 / 72)  # Scale before adding
        
        # Stack those images every 5 frames
        frame_counter += 1
        if frame_counter % 5 == 0:
            stack_img = sum(buffer)  # pixel-wise sum of images
            # Normalize stack image to 8-bit (0-255)
            stack_img = cv2.normalize(stack_img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
            # Write out our stacked image to a file
            cv2.imwrite(f"stacked{frame_counter//5}.jpg", stack_img)
        
        # Clear the stream in preparation for the next frame
        raw_capture.truncate(0)

rolling_long_exposure()
