import cv2
import numpy as np
from ..config.settings import EYE_CASCADE_PATH

class EyeDetector:
    def __init__(self):
        self.eye_cascade = cv2.CascadeClassifier(EYE_CASCADE_PATH)
        self.blink_detected = False
        self.blink_start_time = 0

    def detect_eyes(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eyes = self.eye_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        return len(eyes) >= 1, eyes