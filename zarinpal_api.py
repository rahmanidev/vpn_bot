# zarinpal_api.py
import requests
import json
import os
from datetime import datetime

# مقادیر توی پیام قبلیت
MERCHANT_ID = "6a07e02c-bcc7-4ab8-956d-b28ecd7a5107"
ZARINPAL_REQUEST_URL = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZARINPAL_VERIFY_URL = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZARINPAL_STARTPAY = "https://www.zarinpal.com/pg/StartPay/"
ORDERS_FILE = "orders.json"

def _load_orders():
    if os.path.exists(ORDERS_FILE):
        try:
            with open(ORDERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def _save_orders(data):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def _append_order(order):
    data = _load_orders()
    data.append(order)
    _save_orders(data)

def create_payment(amount_toman, description, user_id=None, callback_url=None):
    """
    amount_toman: integer
    returns dict with keys: url, authority  OR {'error': ...}
    """
    try:
        amount_rial = int(amount_toman) * 10
    except Exception as e:
        return {"error": f"invalid amount: {e}"}

    payload = {
        "merchant_id": MERCHANT_ID,
        "amount": amount_rial,
        "callback_url": callback_url,
        "description": description
    }

    try:
        resp = requests.post(ZARINPAL_REQUEST_URL, json=payload, timeout=15)
        j = resp.json()
    except Exception as e:
        return {"error": f"request error: {e}"}

    # v4 response usually in j["data"]["authority"]
    data = j.get("data") or {}
    authority = data.get("authority")
    if authority:
        url = f"{ZARINPAL_STARTPAY}{authority}"
        order = {
            "authority": authority,
            "user_id": user_id,
            "plan_description": description,
            "amount_toman": int(amount_toman),
            "created_at": datetime.utcnow().isoformat()
        }
        _append_order(order)
        return {"url": url, "authority": authority}
    else:
        return {"error": j}

def verify_payment(authority, amount_rial):
    """
    Verify payment by authority and amount (in RIAL).
    returns response JSON from Zarinpal
    """
    payload = {
        "merchant_id": MERCHANT_ID,
        "authority": authority,
        "amount": amount_rial
    }
    try:
        resp = requests.post(ZARINPAL_VERIFY_URL, json=payload, timeout=15)
        return resp.json()
    except Exception as e:
        return {"error": f"verify request error: {e}"}
