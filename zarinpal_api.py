import requests

MERCHANT_ID = "6a07e02c-bcc7-4ab8-956d-b28ecd7a5107"  # مرچنت کد واقعی خودت رو اینجا بزار
CALLBACK_URL = "https://arsenmobile.com/callback"

def create_payment(amount, description, callback_url):
    url = "https://api.zarinpal.com/pg/v4/payment/request.json"
    data = {
        "merchant_id": MERCHANT_ID,
        "amount": amount,
        "description": description,
        "callback_url": callback_url
        # metadata حذف شد تا خطا نده
    }
    headers = {'accept': 'application/json','content-type': 'application/json'}
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10).json()
        print("ZARINPAL RESPONSE:", response, flush=True)  # لاگ کامل برای بررسی
        if "data" in response and "code" in response["data"] and response['data']['code'] == 100:
            return f"https://www.zarinpal.com/pg/StartPay/{response['data']['authority']}", response['data']['authority']
        else:
            print("Zarinpal Error:", response.get("errors", "Unknown error"), flush=True)
            return None, None
    except Exception as e:
        print("Zarinpal Exception:", e, flush=True)
        return None, None

def verify_payment(authority, amount=100000):
    url = "https://api.zarinpal.com/pg/v4/payment/verify.json"
    data = {
        "merchant_id": MERCHANT_ID,
        "amount": amount,  # باید دقیقاً برابر با مبلغ تراکنش باشه
        "authority": authority
    }
    headers = {'accept': 'application/json','content-type': 'application/json'}
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10).json()
        print("ZARINPAL VERIFY:", response, flush=True)  # لاگ کامل برای بررسی
        if "data" in response and "code" in response["data"] and response['data']['code'] == 100:
            return True
        return False
    except Exception as e:
        print("Zarinpal Verify Exception:", e, flush=True)
        return False
