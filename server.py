# server.py
from flask import Flask, request
import json
import zarinpal_api
from bot_runner import bot  # دقت کن bot_runner.py باید bot را اکسپورت کند
from xui_client import XUIClient
from plans import get_plan_by_id

app = Flask(__name__)

ORDERS_FILE = "orders.json"

def _find_order_by_authority(authority):
    try:
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        return None
    return next((o for o in data if o.get("authority") == authority), None)

@app.route("/callback")
def payment_callback():
    # زرین‌پال ممکنه Authority/Status رو با حروف بزرگ/کوچک ارسال کنه
    authority = request.args.get("Authority") or request.args.get("authority")
    status = request.args.get("Status") or request.args.get("status")
    user_id = request.args.get("user_id")
    plan_id = request.args.get("plan_id")

    order = _find_order_by_authority(authority) if authority else None

    if status == "OK" and order:
        amount_rial = int(order["amount_toman"]) * 10
        verify_resp = zarinpal_api.verify_payment(authority, amount_rial)
        # بررسی موفقیت: در v4 معمولاً کد در verify_resp["data"]["code"] قرار داره
        success = False
        try:
            code = verify_resp.get("data", {}).get("code")
            if code in (100, 101):
                success = True
        except:
            pass
        if success:
            # پرداخت موفق — حالا اکانت در X-UI میسازیم و کانفیگ رو برای کاربر میفرستیم
            bot.send_message(int(user_id), "✅ پرداخت با موفقیت انجام شد. در حال ساخت اکانت...")
            plan = get_plan_by_id(plan_id) if plan_id else None
            xui = XUIClient()
            res = xui.create_client_vmess(remark=f"user_{user_id}_plan{plan_id}", expire_days=(plan["duration_days"] if plan else 30))
            if res.get("ok"):
                # یک پیام ساده با uid بفرست
                uid = res.get("uid")
                bot.send_message(int(user_id), f"اکانت شما ساخته شد.\nUID: {uid}\nبرای دریافت کانفیگ از پنل وارد شوید یا از پشتیبانی درخواست کنید.")
                # (اینجا میشه export config یا اشتراک مستقیم ساخت و ارسال کن)
                return "OK"
            else:
                bot.send_message(int(user_id), f"پرداخت انجام شد اما خطا در ساخت اکانت: {res.get('error')}")
                return "OK"
    # غیرموفق
    if user_id:
        try:
            bot.send_message(int(user_id), "❌ پرداخت ناموفق یا لغو شد.")
        except:
            pass
    return "NOTOK"
