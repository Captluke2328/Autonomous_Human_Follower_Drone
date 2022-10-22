import jetson.inference
import jetson.utils

import cv2
from csi_camera import CSI_Camera

class Camera:
    def __init__(self):
        self.net = jetson.inference.detectNet("SSD-Mobilenet-v2", threshold=0.5)
        
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        
        self.DISPLAY_WIDTH=640
        self.DISPLAY_HEIGHT=320
        self.SENSOR_MODE_720=3
            
    def initializecamera(self):
        self.cam = CSI_Camera()
        self.cam.create_gstreamer_pipeline(
        sensor_id=0,
        sensor_mode=self.SENSOR_MODE_720,
        framerate=30,
        flip_method=6,
        display_height=self.DISPLAY_HEIGHT,
        display_width=self.DISPLAY_WIDTH,
        )
        self.cam.open(self.cam.gstreamer_pipeline)
        self.cam.start()
        
        if (not self.cam.video_capture.isOpened()):
            print("Unable to open any cameras")
            SystemExit(0)
            
        return self.cam