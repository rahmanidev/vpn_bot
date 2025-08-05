from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from zarinpal_api import create_payment

TOKEN = "8365218010:AAFeYmsmSeDCmpJzSV_A7AFLhrYzvzS7_RU"
CALLBACK_URL = "https://nuvix.ir/vpn_callback/callback"

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

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buy_menu, pattern="buy_menu"))
    app.add_handler(CallbackQueryHandler(process_buy, pattern="buy_"))
    print("ربات شروع به کار کرد ...")
    app.run_polling()

if __name__ == "__main__":
    main()
