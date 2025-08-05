import requests

MERCHANT_ID = "6a07e02c-bcc7-4ab8-956d-b28ecd7a5107"

def create_payment(amount, description, callback_url, email="", mobile=""):
    url = "https://api.zarinpal.com/pg/v4/payment/request.json"
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
        print("ZARINPAL RESPONSE:", response)
        if "data" in response and "code" in response["data"] and response['data']['code'] == 100:
            return f"https://www.zarinpal.com/pg/StartPay/{response['data']['authority']}", response['data']['authority']
        else:
            print("Zarinpal Error:", response.get("errors", "Unknown error"))
            return None, None
    except Exception as e:
        print("Zarinpal Exception:", e)
        return None, None
