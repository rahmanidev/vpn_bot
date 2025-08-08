# bot_runner.py
import threading
from callback import bot  # bot را از callback.py می‌گیریم
from server import app
import time

def run_bot():
    # polling bot
    bot.infinity_polling(timeout=60, long_polling_timeout=60)

def run_server():
    # flask app
    app.run(host="0.0.0.0", port=5000, threaded=True)

if __name__ == "__main__":
    t1 = threading.Thread(target=run_bot, daemon=True)
    t2 = threading.Thread(target=run_server, daemon=True)
    t1.start()
    t2.start()
    # نگه داشتن پروسس
    while True:
        time.sleep(60)
