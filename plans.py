# plans.py
# لیست پلن‌ها — از ID=1 تا 8 مطابق درخواستی که گفتی
PLANS = [
    {"id": "1", "title": "یک ماهه — 30 گیگ — کاربر نامحدود", "duration_days": 30, "bandwidth_gb": 30, "users": "نامحدود", "price_toman": 110000},
    {"id": "2", "title": "یک ماهه — 50 گیگ — کاربر نامحدود", "duration_days": 30, "bandwidth_gb": 50, "users": "نامحدود", "price_toman": 190000},
    {"id": "3", "title": "یک ماهه — حجم نامحدود — تک کاربر", "duration_days": 30, "bandwidth_gb": None, "users": 1, "price_toman": 220000},
    {"id": "4", "title": "یک ماهه — حجم نامحدود — دو کاربر", "duration_days": 30, "bandwidth_gb": None, "users": 2, "price_toman": 350000},
    {"id": "5", "title": "دو ماهه — 70 گیگ — کاربر نامحدود", "duration_days": 60, "bandwidth_gb": 70, "users": "نامحدود", "price_toman": 250000},
    {"id": "6", "title": "یک ماهه — 100 گیگ — کاربر نامحدود", "duration_days": 30, "bandwidth_gb": 100, "users": "نامحدود", "price_toman": 350000},
    {"id": "7", "title": "سه ماهه — 150 گیگ — کاربر نامحدود", "duration_days": 90, "bandwidth_gb": 150, "users": "نامحدود", "price_toman": 450000},
    {"id": "8", "title": "سه ماهه — 300 گیگ — کاربر نامحدود", "duration_days": 90, "bandwidth_gb": 300, "users": "نامحدود", "price_toman": 850000},
]

def get_plan_by_id(pid):
    return next((p for p in PLANS if str(p["id"]) == str(pid)), None)
