from flask import Flask, request
from zarinpal_api import verify_payment
import json

app = Flask(__name__)

@app.route('/zarinpal/callback')
def zarinpal_callback():
    authority = request.args.get('Authority')
    status = request.args.get('Status')

    with open("data.json","r") as f:
        data = json.load(f)
    
    user_id = None
    for uid, info in data.items():
        if info.get("authority") == authority:
            user_id = uid
            break

    if status == 'OK' and user_id:
        amount = 100000 if data[user_id]['plan'] == "1" else 250000
        result = verify_payment(amount, authority)
        if result['data']['code'] == 100:
            data[user_id]['status'] = "active"
            with open("data.json","w") as f:
                json.dump(data,f)
            return "پرداخت موفق بود. سرویس فعال شد."
        else:
            return "پرداخت تأیید نشد."
    else:
        return "پرداخت لغو شد."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
