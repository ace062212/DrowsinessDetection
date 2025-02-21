import requests
from ..config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        params = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "notification": True
        }
        response = requests.get(url, params=params)
        return response.status_code == 200
    except Exception as e:
        print(f"Telegram notification error: {e}")
        return False