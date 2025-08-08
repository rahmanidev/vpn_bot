from telebot import TeleBot, types
import requests

# تنظیمات ثابت
TOKEN = "8365218010:AAFeYmsmSeDCmpJzSV_A7AFLhrYzvzS7_RU"
MERCHANT_ID_zarinpal = "6a07e02c-bcc7-4ab8-956d-b28ecd7a5107"
CALLBACK_URL = "https://arsenmobile.com/callback"

bot = TeleBot(TOKEN)

plans = [
    {"title": "یک ماهه ، 30 گیگ ، کاربر نامحدود", "price": 110000, "period": 30, "traffic": 30, "users": "نامحدود"},
    {"title": "یک ماهه ، 50 گیگ ، کاربر نامحدود", "price": 190000, "period": 30, "traffic": 50, "users": "نامحدود"},
    {"title": "یک ماهه ، حجم نامحدود ، تک کاربر", "price": 220000, "period": 30, "traffic": -1, "users": "1"},
    {"title": "یک ماهه ، حجم نامحدود ، دو کاربر", "price": 350000, "period": 30, "traffic": -1, "users": "2"},
    {"title": "دو ماهه ، 70 گیگ ، کاربر نامحدود", "price": 250000, "period": 60, "traffic": 70, "users": "نامحدود"},
    {"title": "یک ماهه ، 100 گیگ ، کاربر نامحدود", "price": 350000, "period": 30, "traffic": 100, "users": "نامحدود"},
    {"title": "سه ماهه ، 150 گیگ ، کاربر نامحدود", "price": 450000, "period": 90, "traffic": 150, "users": "نامحدود"},
    {"title": "سه ماهه ، 300 گیگ ، کاربر نامحدود", "price": 850000, "period": 90, "traffic": 300, "users": "نامحدود"},
]

# یک دیتابیس ساده موقت (مثلا dict) برای ذخیره سرویس‌ها (برای نمونه)
user_services = {}

def create_payment_link(amount, description, user_id):
    url = "https://api.zarinpal.com/pg/v4/payment/request.json"
    data = {
        "merchant_id": MERCHANT_ID_zarinpal,
        "amount": amount,
        "callback_url": CALLBACK_URL,
        "description": description,
        "metadata": {"user_id": user_id}
    }
    response = requests.post(url, json=data)
    if response.status_code == 200 and response.json().get("data", {}).get("authority"):
        authority = response.json()["data"]["authority"]
        return f"https://www.zarinpal.com/pg/StartPay/{authority}"
    else:
        return None

def build_panel_for_user(user_id, plan):
    # این تابع باید به پنل XUI یا پنل وی‌پی‌ان متصل بشه و اکانت بسازه
    # الان فقط یک رشته نمونه برمیگردونه:
    return f"اکانت شما ساخته شد:\nپلن: {plan['title']}\nکاربر: {user_id}"

@bot.message_handler(commands=['start'])
def start_handler(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🛒 خرید سرویس", callback_data="buy_service"))
    keyboard.add(types.InlineKeyboardButton("📊 وضعیت سرویس", callback_data="status_service"))
    keyboard.add(types.InlineKeyboardButton("🔄 تمدید سرویس", callback_data="renew_service"))
    bot.send_message(message.chat.id, "سلام! گزینه مورد نظر را انتخاب کنید:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "buy_service":
        send_plans(call.message)
    elif call.data == "status_service":
        show_status(call.message)
    elif call.data == "renew_service":
        renew_service(call.message)
    elif call.data.startswith("plan_"):
        plan_selected(call)

def send_plans(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for i, plan in enumerate(plans, 1):
        text = f"{plan['title']} - {plan['price']} تومان"
        btn = types.InlineKeyboardButton(text, callback_data=f"plan_{i}")
        keyboard.add(btn)
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                          text="لطفا پلن مورد نظر خود را انتخاب کنید:", reply_markup=keyboard)

def show_status(message):
    user_id = message.chat.id
    service = user_services.get(user_id)
    if service:
        text = f"وضعیت سرویس شما:\nپلن: {service['plan']['title']}\nمانده حجم: {service.get('remaining_traffic', 'نامعلوم')}\nمانده روز: {service.get('remaining_days', 'نامعلوم')}"
    else:
        text = "شما سرویس فعالی ندارید."
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text)

def renew_service(message):
    # همین خرید سرویس رو نشون بده (یا میتونی منطق تمدید اضافه کنی)
    send_plans(message)

def plan_selected(call):
    user_id = call.message.chat.id
    plan_index = int(call.data.split("_")[1]) - 1
    plan = plans[plan_index]

    payment_link = create_payment_link(plan["price"], plan["title"], user_id)
    if payment_link:
        bot.answer_callback_query(call.id, f"لطفا پرداخت را انجام دهید.")
        bot.send_message(user_id, f"برای پرداخت پلن «{plan['title']}» لطفا روی لینک زیر کلیک کنید:\n{payment_link}")
        # فرض می‌کنیم بعد پرداخت callback میزنه و اکانت ساخته میشه
    else:
        bot.answer_callback_query(call.id, "مشکل در ایجاد لینک پرداخت. لطفا بعدا تلاش کنید.")

# فرض کنیم بعد از callback زرین پال این تابع فراخوانی میشه (شبیه‌سازی)
def payment_success(user_id, plan_index):
    plan = plans[plan_index]
    user_services[user_id] = {
        "plan": plan,
        "remaining_traffic": plan["traffic"],
        "remaining_days": plan["period"],
    }
    panel_info = build_panel_for_user(user_id, plan)
    bot.send_message(user_id, panel_info)

if __name__ == "__main__":
    print("Starting bot...")
    bot.infinity_polling()
