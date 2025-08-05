from flask import Flask, request
from zarinpal_api import verify_payment

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Server is running!", 200

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

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
