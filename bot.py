import os
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from zarinpal_api import create_payment, verify_payment

TOKEN = "8365218010:AAFeYmsmSeDCmpJzSV_A7AFLhrYzvzS7_RU"
CALLBACK_URL = "https://nuvix.ir/vpn_callback/callback"

# ساخت اپ Flask و اپ تلگرام
app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

# حلقه رویداد سازگار با Python 3.12
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(application.initialize())
loop.run_until_complete(application.start())


# --- /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛒 خرید سرویس", callback_data='buy_menu')],
        [InlineKeyboardButton("📊 وضعیت سرویس", callback_data='status')],
        [InlineKeyboardButton("🔄 تمدید سرویس", callback_data='renew')]
    ]
    await update.message.reply_text(
        "به ربات خوش اومدی! لطفاً یکی از گزینه‌ها رو انتخاب کن:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- خرید ---
async def buy_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("🛒 خرید سرویس 1 ماهه", callback_data='buy_1')],
        [InlineKeyboardButton("🛒 خرید سرویس 3 ماهه", callback_data='buy_3')]
    ]
    await query.edit_message_text(
        "لطفاً یکی از پلن‌ها رو انتخاب کن:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def process_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    plan = query.data.split("_")[1]
    amount = 100000 if plan == "1" else 250000
    url, authority = create_payment(amount, f"خرید سرویس {plan} ماهه", CALLBACK_URL)
    if url:
        await query.edit_message_text(f"برای پرداخت روی لینک زیر کلیک کن:\n{url}")
    else:
        await query.edit_message_text("❌ خطا در ایجاد تراکنش. لطفاً دوباره تلاش کنید.")

# --- هندلرها ---
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(buy_menu, pattern="buy_menu"))
application.add_handler(CallbackQueryHandler(process_buy, pattern="buy_"))

# --- Webhook (GET برای تست + POST برای تلگرام) ---
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        return "Webhook OK", 200
    data = request.get_json(force=True)
    print("RAW UPDATE:", data)  # برای دیباگ تو لاگ Railway
    update = Update.de_json(data, application.bot)
    loop.create_task(application.process_update(update))
    return "OK", 200

# --- Callback زرین‌پال ---
@app.route("/callback", methods=["GET"])
def callback():
    authority = request.args.get('Authority')
    status = request.args.get('Status')
    if status == "OK":
        verified = verify_payment(authority)
        if verified:
            return "پرداخت شما با موفقیت انجام شد.", 200
        else:
            return "پرداخت تایید نشد!", 200
    return "پرداخت لغو شد!", 200

# --- صفحه اصلی ---
@app.route("/", methods=["GET"])
def home():
    return "Bot is running!", 200

# اجرای Flask روی پورت Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
