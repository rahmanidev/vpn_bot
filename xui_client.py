# xui_client.py
import requests
import uuid
import time

# تنظیمات X-UI از پیامت
XUI_BASE = "http://arsenmobile.armani19.space:9537"  # بدون / در پایان
XUI_USER = "2020ar"
XUI_PASS = "2020ss"
# لیست پورت‌هایی که گفتی: تلاش می‌کنیم با یکی از اینها استفاده کنیم
XUI_POSSIBLE_PORTS = [9537, 2096]

class XUIClient:
    def __init__(self, base=XUI_BASE, username=XUI_USER, password=XUI_PASS):
        self.base = base.rstrip("/")
        self.username = username
        self.password = password
        self.s = requests.Session()
        self.logged = False

    def login(self):
        """
        سعی می‌کنیم با فرمی که اکثر پنل‌ها دارند لاگین کنیم.
        در بعضی پنل‌ها endpoint ممکنه /login یا /auth/login باشه — اگر لاگین نشد پیام خطا برمی‌گردانیم.
        """
        # Try common login endpoints
        tries = ["/login", "/auth/login", "/api/v1/login"]
        for ep in tries:
            url = self.base + ep
            try:
                resp = self.s.post(url, data={"username": self.username, "password": self.password}, timeout=8, allow_redirects=True)
                text = resp.text.lower()
                # heuristics: اگر redirect شد یا در جواب "token" یا "ok" دیده شد
                if resp.status_code in (200, 302) and ("dashboard" in text or resp.status_code == 302 or "token" in text or "ok" in text):
                    self.logged = True
                    return True
            except Exception:
                pass
        # fallback: try basic auth on GET of base
        try:
            resp = self.s.get(self.base, auth=(self.username, self.password), timeout=6)
            if resp.status_code == 200:
                self.logged = True
                return True
        except Exception:
            pass

        return False

    def create_client_vmess(self, remark=None, expire_days=30, inbound_port=None, flow=None):
        """
        سعی می‌کنه یک client/vmess بسازه و لینک یا جزئیات برگردونه.
        توجه: ساختار payload ممکنه بسته به نسخه پنل مقداردهی متفاوت باشه — اگر پیغام خطا دیدی به من بگو تا دقیقاً payload رو برای پنل شما اصلاح کنم.
        """
        if not self.logged and not self.login():
            return {"error": "login failed to x-ui panel"}

        # payload پایه برای بیشتر پنل‌ها
        uid = str(uuid.uuid4())
        remark = remark or f"user-{int(time.time())}"
        inbound_port = inbound_port or (XUI_POSSIBLE_PORTS[0] if XUI_POSSIBLE_PORTS else None)

        payload = {
            "remark": remark,
            "listen": inbound_port,
            "protocol": "vmess",
            "settings": {
                "clients": [
                    {
                        "id": uid,
                        "alterId": 0,
                        "email": remark
                    }
                ]
            },
            # expires/traffic fields may differ — server-side logic ممکنه نیاز به fields دیگر داشته باشد
            "expiry_time": expire_days  # ممکن است پنل این نام را نپذیرد؛ در آن صورت باید مطابق docs تغییر کند
        }

        # Try likely API endpoints for adding inbound/client
        endpoints = [
            "/inbounds/add", "/inbounds", "/api/v1/inbounds", "/api/inbounds/add", "/v1/inbound/add", "/vip/panel/inbounds"
        ]
        for ep in endpoints:
            url = self.base + ep
            try:
                r = self.s.post(url, json=payload, timeout=10)
                try:
                    j = r.json()
                except:
                    j = {"status_code": r.status_code, "text": r.text}
                # heuristics: اگر موفق یا id برگشته
                if r.status_code in (200, 201) and (isinstance(j, dict) and ("success" in j or "id" in j or r.status_code == 201)):
                    return {"ok": True, "response": j, "uid": uid}
                # بعضی پنل‌ها پاسخ متن ساده می‌دهند
                if r.status_code in (200,201):
                    return {"ok": True, "response_text": r.text, "uid": uid}
            except Exception as e:
                # ادامه بده و endpoint بعدی رو امتحان کن
                last_err = str(e)
                continue

        return {"error": "could not create inbound - endpoints tried", "last_err": locals().get("last_err", "")}
