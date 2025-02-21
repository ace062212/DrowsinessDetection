import numpy as np
import mediapipe as mp
from ..config.settings import MOUTH_LANDMARKS

class MouthDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            min_detection_confidence=0.5
        )

    def calculate_mouth_ratio(self, mouth_points):
        hor_distance = np.linalg.norm(np.array(mouth_points[3]) - np.array(mouth_points[5]))
        ver_distance = np.linalg.norm(np.array(mouth_points[1]) - np.array(mouth_points[2]))
        return ver_distance / hor_distance if hor_distance != 0 else 0

    def detect_mouth(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                mouth_points = [
                    (int(face_landmarks.landmark[idx].x * frame.shape[1]),
                     int(face_landmarks.landmark[idx].y * frame.shape[0]))
                    for idx in MOUTH_LANDMARKS
                ]
                ratio = self.calculate_mouth_ratio(mouth_points)
                return ratio > 1, mouth_points
        return False, None