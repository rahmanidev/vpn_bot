# callback.py
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from plans import PLANS, get_plan_by_id
import zarinpal_api
from xui_client import XUIClient
import os

# از تنظیماتی که دادی استفاده می‌کنیم
TOKEN = "8365218010:AAFeYmsmSeDCmpJzSV_A7AFLhrYzvzS7_RU"
CALLBACK_URL_BASE = "https://arsenmobile.com/callback"  # اگر مسیر متفاوتی میخوای اینجا عوض کن
SERVER_IP = "156.253.5.251"
ADMIN_CHAT_ID = 5727187871

bot = telebot.TeleBot(TOKEN)

def build_plans_keyboard():
    kb = InlineKeyboardMarkup()
    for p in PLANS:
        label = f"{p['title']} — {p['price_toman']:,} تومان"
        kb.add(InlineKeyboardButton(label, callback_data=f"plan_{p['id']}"))
    kb.add(InlineKeyboardButton("🔙 بازگشت", callback_data="main_menu"))
    return kb

@bot.message_handler(commands=["start", "menu"])
def send_welcome(m):
    txt = "سلام — خوش اومدی!\nبرای خرید اشتراک از دکمه‌ی زیر استفاده کن."
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🛒 خرید اشتراک", callback_data="buy_subscription"))
    bot.send_message(m.chat.id, txt, reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data == "buy_subscription")
def show_plans(call):
    kb = build_plans_keyboard()
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text="لطفا پلن مورد نظر را انتخاب کن:",
                          reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data and call.data.startswith("plan_"))
def handle_plan_selection(call):
    pid = call.data.split("_", 1)[1]
    plan = get_plan_by_id(pid)
    if not plan:
        bot.answer_callback_query(call.id, "پلن پیدا نشد ❌")
        return

    # callback url زرین پال — زرین‌پال به همین آدرس بازمی‌گردد
    # ما user_id و plan_id رو query می‌فرستیم تا در callback بشه فعال‌سازی رو انجام داد
    callback_url = f"{CALLBACK_URL_BASE}?user_id={call.from_user.id}&plan_id={pid}"

    payment = zarinpal_api.create_payment(amount_toman=plan["price_toman"],
                                          description=f"خرید اشتراک — {plan['title']}",
                                          user_id=call.from_user.id,
                                          callback_url=callback_url)
    if payment.get("url"):
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=f"برای پرداخت، روی لینک زیر کلیک کن:\n{payment['url']}\n\nبعد از پرداخت منتظر بمون تا اشتراک فعال بشه.",
                              disable_web_page_preview=True)
    else:
        bot.answer_callback_query(call.id, "خطا در ساخت درگاه پرداخت — بعدا تلاش کن.")
