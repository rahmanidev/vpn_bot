from flask import Flask, request, jsonify

app = Flask(__name__)

MERCHANT_ID_zarinpal = "6a07e02c-bcc7-4ab8-956d-b28ecd7a5107"
CALLBACK_URL = "https://arsenmobile.com/callback"
TOKEN_telegram_bot = "8365218010:AAFeYmsmSeDCmpJzSV_A7AFLhrYzvzS7_RU"
server_ip = "156.253.5.251"

# اگر لازم بود به بات دسترسی داشته باشی، فقط داخل فانکشن ایمپورت کن:
def get_bot():
    from bot_runner import bot
    return bot

@app.route('/')
def index():
    return "Server is running"

# نمونه API برای کال بک پرداخت زرین پال
@app.route('/callback', methods=['GET', 'POST'])
def payment_callback():
    # اینجا باید منطق تایید پرداخت و پردازش رو بنویسی
    # فرض می‌کنیم فقط یه پاسخ ساده میدیم
    data = request.args.to_dict()
    # می‌تونی اینجا منطق زارین پال رو اضافه کنی
    return jsonify({"status": "callback received", "data": data})
