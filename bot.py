from telegram import Bot
import time
from datetime import datetime

def send_news():
    bot = Bot(token="TU_TOKEN_DE_TELEGRAM")
    chat_id = "TU_CHAT_ID"
    news = get_news()  # Usa la misma función que en app.py
    for article in news[:5]:  # Envía las primeras 5 noticias
        bot.send_message(chat_id=chat_id, text=article["title"] + "\n" + article["url"])

def main():
    while True:
        now = datetime.now()
        if now.hour == 8 and now.minute == 0:  # Envía noticias a las 8:00 AM
            send_news()
            time.sleep(60)  # Espera 1 minuto para evitar múltiples envíos
        time.sleep(30)  # Revisa cada 30 segundos

if __name__ == "__main__":
    main()
