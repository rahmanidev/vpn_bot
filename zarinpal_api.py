import requests

MERCHANT_ID = "6a07e02c-bcc7-4ab8-956d-b28ecd7a5107"  # مطمئن شو این همون مرچنت واقعی زرین‌پاله

def create_payment(amount, description, callback_url, email="", mobile=""):
    url = "https://api.zarinpal.com/pg/v4/payment/request.json"  # برای SandBox: https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json
    data = {
        "merchant_id": MERCHANT_ID,
        "amount": amount,
        "description": description,
        "callback_url": callback_url,
        "metadata": {"email": email, "mobile": mobile}
    }
    headers = {'accept': 'application/json','content-type': 'application/json'}
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10).json()
        print("ZARINPAL RESPONSE:", response, flush=True)  # لاگ کامل پاسخ
        if "data" in response and "code" in response["data"] and response['data']['code'] == 100:
            return f"https://www.zarinpal.com/pg/StartPay/{response['data']['authority']}", response['data']['authority']
        else:
            # لاگ خطا
            print("Zarinpal Error:", response.get("errors", "Unknown error"), flush=True)
            return None, None
    except Exception as e:
        print("Zarinpal Exception:", e, flush=True)
        return None, None

def verify_payment(authority):
    url = "https://api.zarinpal.com/pg/v4/payment/verify.json"  # برای SandBox: https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json
    data = {
        "merchant_id": MERCHANT_ID,
        "amount": 100000,  # این باید دقیقاً همون مبلغ تراکنش باشه
        "authority": authority
    }
    headers = {'accept': 'application/json','content-type': 'application/json'}
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10).json()
        print("ZARINPAL VERIFY:", response, flush=True)  # لاگ کامل پاسخ
        if "data" in response and "code" in response["data"] and response['data']['code'] == 100:
            return True
        return False
    except Exception as e:
        print("Zarinpal Verify Exception:", e, flush=True)
        return False
