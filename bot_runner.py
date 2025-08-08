from telebot import TeleBot
from server import app

TOKEN = "8365218010:AAFeYmsmSeDCmpJzSV_A7AFLhrYzvzS7_RU"
bot = TeleBot(TOKEN)

# لیست پلن‌ها (اینها رو تو خودت میتونی اصلاح و کامل کنی)
plans = [
    {"title": "یک ماهه ، 30 گیگ ، کاربر نامحدود", "price": "110000"},
    {"title": "یک ماهه ، 50 گیگ ، کاربر نامحدود", "price": "190000"},
    {"title": "یک ماهه ، حجم نامحدود ، تک کاربر", "price": "220000"},
    {"title": "یک ماهه ، حجم نامحدود ، دو کاربر", "price": "350000"},
    {"title": "دو ماهه ، 70 گیگ ، کاربر نامحدود", "price": "250000"},
    {"title": "یک ماهه ، 100 گیگ ، کاربر نامحدود", "price": "350000"},
    {"title": "سه ماهه ، 150 گیگ ، کاربر نامحدود", "price": "450000"},
    {"title": "سه ماهه ، 300 گیگ ، کاربر نامحدود", "price": "850000"},
]

@bot.message_handler(commands=['start'])
def start_handler(message):
    text = "سلام! به ربات VPN خوش آمدید.\nبرای خرید اشتراک یکی از گزینه‌های زیر را انتخاب کنید:\n\n"
    for i, plan in enumerate(plans, 1):
        text += f"{i}. {plan['title']} - {plan['price']} تومان\n"
    bot.send_message(message.chat.id, text)

# اینجا میتونی هندرهای بیشتری برای پردازش خرید و پرداخت اضافه کنی

if __name__ == "__main__":
    print("Starting bot...")
    bot.infinity_polling()
