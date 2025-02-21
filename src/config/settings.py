# GPIO 설정
BUZZER_PIN = 18

# 화면 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 감지 설정
YAWN_THRESHOLD_TIME = 2  # seconds
BLINK_TEXT_TIME = 1  # seconds
MOUTH_LANDMARKS = [61, 291, 0, 17, 78, 308]

# 카메라 설정
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Haar Cascade 파일 경로
EYE_CASCADE_PATH = '/home/sw2024/Desktop/haarcascade_eye.xml'

# API 키 (실제 값은 환경변수나 별도 설정 파일로 관리)
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

# 데이터베이스 설정
DB_CONFIG = {
    "host": "best.hnu.kr",
    "user": "user_sw2024",
    "password": "sw2024",
    "db": "db_sw2024",
    "charset": "utf8"
}