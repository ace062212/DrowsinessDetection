import cv2
import time
import RPi.GPIO as GPIO
from picamera2 import Picamera2
from .utils.display import Display
from .utils.notification import send_telegram_message
from .utils.database import upload_to_database
from .detection.eye_detector import EyeDetector
from .detection.mouth_detector import MouthDetector
from .config.settings import BUZZER_PIN, YAWN_THRESHOLD_TIME, BLINK_TEXT_TIME

class DrowsinessDetectionSystem:
    def __init__(self):
        # Initialize display
        self.display = Display()
        
        # Initialize camera
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration(
            main={"size": (640, 480)}))
        
        # Initialize detectors
        self.eye_detector = EyeDetector()
        self.mouth_detector = MouthDetector()
        
        # Initialize GPIO for buzzer
        self.setup_buzzer()
        
        # Initialize variables
        self.speed = 0
        self.eye_detection_active = False
        self.yawn_count = 0
        self.yawn_detected = False
        self.yawn_start_time = 0
        self.key_w_pressed = False
        self.key_s_pressed = False

    def setup_buzzer(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUZZER_PIN, GPIO.OUT)
        GPIO.setwarnings(False)
        self.pwm = GPIO.PWM(BUZZER_PIN, 1.0)
        self.pwm.start(50.0)
        self.pwm.ChangeDutyCycle(0.0)

    def trigger_buzzer(self, duration):
        self.pwm.ChangeFrequency(2500)
        self.pwm.ChangeDutyCycle(50.0)
        time.sleep(duration)
        self.pwm.ChangeDutyCycle(0.0)

    def trigger_notification_buzzer(self):
        self.pwm.ChangeFrequency(500)
        self.pwm.ChangeDutyCycle(50.0)
        time.sleep(0.5)
        self.pwm.ChangeDutyCycle(0.0)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.key_w_pressed = True
                elif event.key == pygame.K_s:
                    self.key_s_pressed = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.key_w_pressed = False
                elif event.key == pygame.K_s:
                    self.key_s_pressed = False
        return True

    def update_speed(self):
        if self.key_w_pressed:
            self.speed += 2
        if self.key_s_pressed:
            self.speed -= 1
        if self.speed < 0:
            self.speed = 0

    def process_frame(self, frame):
        # Eye detection
        eyes_open, _ = self.eye_detector.detect_eyes(frame)
        if not eyes_open:
            if not self.eye_detector.blink_detected:
                self.eye_detector.blink_start_time = time.time()
                self.eye_detector.blink_detected = True
            elif time.time() - self.eye_detector.blink_start_time >= BLINK_TEXT_TIME:
                self.trigger_buzzer(1.0)
                send_telegram_message("운전자의 눈감음으로 졸음이 판단되었습니다. 신속한 조치가 필요한 상황입니다!!!!")
                upload_to_database(0, 1)
        else:
            self.eye_detector.blink_detected = False

        # Mouth detection
        is_yawning, mouth_points = self.mouth_detector.detect_mouth(frame)
        if is_yawning:
            current_time = time.time()
            if not self.yawn_detected and (current_time - self.yawn_start_time > YAWN_THRESHOLD_TIME):
                self.yawn_count += 1
                self.yawn_detected = True
                self.yawn_start_time = current_time
                if self.yawn_count >= 3:
                    self.trigger_buzzer(1.0)
                    send_telegram_message("운전자가 하품을 3회 하였습니다.")
                    upload_to_database(1, 0)
                    self.yawn_count = 0
        else:
            self.yawn_detected = False

        # Draw on frame
        self.draw_info_on_frame(frame, eyes_open)
        return frame

    def draw_info_on_frame(self, frame, eyes_open):
        cv2.putText(frame, f'Yawns: {self.yawn_count}', 
                   (50, frame.shape[0] - 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        eye_status = "Eyes closed" if not eyes_open else "Eyes open"
        eye_color = (0, 0, 255) if not eyes_open else (0, 255, 0)
        cv2.putText(frame, eye_status, (50, 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, eye_color, 2)

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update_speed()
            
            # Activate/deactivate detection based on speed
            if self.speed >= 30:
                if not self.eye_detection_active:
                    self.picam2.start()
                    self.eye_detection_active = True
                    self.trigger_notification_buzzer()
            else:
                if self.eye_detection_active:
                    self.picam2.stop()
                    self.eye_detection_active = False

            # Process camera frame if active
            if self.eye_detection_active:
                frame = self.picam2.capture_array()
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                frame = self.process_frame(frame)
                cv2.imshow('Eye and Mouth Detection', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    running = False

            # Update display
            self.display.update_display(self.speed)
            pygame.time.Clock().tick(30)

    def cleanup(self):
        self.display.cleanup()
        self.picam2.stop()
        cv2.destroyAllWindows()
        GPIO.cleanup()

if __name__ == "__main__":
    system = DrowsinessDetectionSystem()
    try:
        system.run()
    finally:
        system.cleanup()