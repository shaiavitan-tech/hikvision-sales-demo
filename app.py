from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# -----------------------------
# Data layer (מדמה DB)
# -----------------------------

products = {
    "ip_cam_4mp_basic": {
        "id": "ip_cam_4mp_basic",
        "name": "מצלמת IP 4MP ColorVu בסיסית",
        "category": "Camera IP",
        "type": "Main",
        "list_price_estimate": 800,
    },
    "ip_cam_4mp_pro": {
        "id": "ip_cam_4mp_pro",
        "name": "מצלמת IP 4MP ColorVu AcuSense",
        "category": "Camera IP",
        "type": "Main",
        "list_price_estimate": 1100,
    },
    "turbohd_cam_2mp": {
        "id": "turbohd_cam_2mp",
        "name": "מצלמת Turbo HD 2MP",
        "category": "Camera Analog",
        "type": "Main",
        "list_price_estimate": 500,
    },
    "nvr_8ch_entry": {
        "id": "nvr_8ch_entry",
        "name": "NVR ל-8 ערוצים",
        "category": "NVR",
        "type": "Main",
        "list_price_estimate": 1500,
    },
    "nvr_16ch_pro": {
        "id": "nvr_16ch_pro",
        "name": "NVR ל-16 ערוצים",
        "category": "NVR",
        "type": "Main",
        "list_price_estimate": 2500,
    },
    "dvr_8ch_entry": {
        "id": "dvr_8ch_entry",
        "name": "DVR ל-8 ערוצים",
        "category": "DVR",
        "type": "Main",
        "list_price_estimate": 1200,
    },
    "poe_switch_8": {
        "id": "poe_switch_8",
        "name": "מתג PoE 8 פורטים Hikvision",
        "category": "Networking",
        "type": "Accessory",
        "list_price_estimate": 700,
    },
    "poe_switch_16": {
        "id": "poe_switch_16",
        "name": "מתג PoE 16 פורטים Hikvision",
        "category": "Networking",
        "type": "Accessory",
        "list_price_estimate": 1300,
    },
    "hdd_2tb": {
        "id": "hdd_2tb",
        "name": "דיסק 2TB למערכות NVR/DVR",
        "category": "Storage",
        "type": "Accessory",
        "list_price_estimate": 400,
    },
    "hdd_4tb": {
        "id": "hdd_4tb",
        "name": "דיסק 4TB למערכות NVR/DVR",
        "category": "Storage",
        "type": "Accessory",
        "list_price_estimate": 650,
    },
    "ups_small": {
        "id": "ups_small",
        "name": "UPS קטן למערכת ביתית/SMB",
        "category": "Power",
        "type": "Accessory",
        "list_price_estimate": 900,
    },
    "ups_medium": {
        "id": "ups_medium",
        "name": "UPS בינוני למשרד/מחסן",
        "category": "Power",
        "type": "Accessory",
        "list_price_estimate": 1400,
    },
    "cam_mount_wall": {
        "id": "cam_mount_wall",
        "name": "מתאם קיר/עמוד למצלמה",
        "category": "CCTV Accessory",
        "type": "Accessory",
        "list_price_estimate": 250,
    },
    "cam_junction_box": {
        "id": "cam_junction_box",
        "name": "קופסת חיבורים למצלמה",
        "category": "CCTV Accessory",
        "type": "Accessory",
        "list_price_estimate": 220,
    },
    "cam_pendant_mount": {
        "id": "cam_pendant_mount",
        "name": "מתאם תלייה/תקרה למצלמה",
        "category": "CCTV Accessory",
        "type": "Accessory",
        "list_price_estimate": 260,
    },
    "access_ctrl_basic": {
        "id": "access_ctrl_basic",
        "name": "בקר גישה בסיסי (4 דלתות)",
        "category": "Access Control",
        "type": "Main",
        "list_price_estimate": 1800,
    },
    "door_lock_basic": {
        "id": "door_lock_basic",
        "name": "מנעול חשמלי לדלת גישה",
        "category": "Access Control",
        "type": "Accessory",
        "list_price_estimate": 600,
    },
    "door_contact": {
        "id": "door_contact",
        "name": "מגנט דלת (Door Contact)",
        "category": "Access Control",
        "type": "Accessory",
        "list_price_estimate": 150,
    },
    "intercom_door_station": {
        "id": "intercom_door_station",
        "name": "תחנת אינטרקום כניסה וידאו",
        "category": "Intercom",
        "type": "Main",
        "list_price_estimate": 1600,
    },
    "intercom_room_station": {
        "id": "intercom_room_station",
        "name": "תחנת אינטרקום חדר",
        "category": "Intercom",
        "type": "Accessory",
        "list_price_estimate": 900,
    },
}

# פרופילי לקוח – מסונכרן ל-UI
customers = {
    "home": {
        "id": "home",
        "name": "משפחה בבית פרטי",
        "segment": "בית פרטי",
        "installed": [
            {"product_id": "ip_cam_4mp_basic", "count": 3},
            {"product_id": "nvr_8ch_entry", "count": 1},
        ],
    },
    "store": {
        "id": "store",
        "name": "חנות אופנה קטנה",
        "segment": "עסק קטן",
        "installed": [
            {"product_id": "ip_cam_4mp_pro", "count": 2},
            {"product_id": "ip_cam_4mp_basic", "count": 2},
            {"product_id": "nvr_16ch_pro", "count": 1},
            {"product_id": "poe_switch_8", "count": 1},
        ],
    },
    "office": {
        "id": "office",
        "name": "משרד / הייטק קטן",
        "segment": "משרד",
        "installed": [
            {"product_id": "ip_cam_4mp_pro", "count": 4},
            {"product_id": "nvr_16ch_pro", "count": 1},
            {"product_id": "access_ctrl_basic", "count": 1},
            {"product_id": "door_lock_basic", "count": 1},
        ],
    },
    "warehouse": {
        "id": "warehouse",
        "name": "מחסן / לוגיסטיקה קטנה",
        "segment": "מחסן",
        "installed": [
            {"product_id": "ip_cam_4mp_basic", "count": 2},
            {"product_id": "turbohd_cam_2mp", "count": 2},
            {"product_id": "dvr_8ch_entry", "count": 1},
        ],
    },
}

# חוקים – כמו בטבלה, rule-based
cross_sell_rules = {
    "ip_cam_4mp_basic": {
        "recommended": [
            "cam_mount_wall",
            "cam_junction_box",
            "poe_switch_8",
            "hdd_2tb",
            "ups_small",
        ],
        "tagline": "שדרוג אמינות והתקנה",
        "description": "אביזרי התקנה, רשת ואחסון לשדרוג מערכת המצלמות הבסיסית.",
        "benefits": [
            "הגנה על חיבורים",
            "המשך הקלטה בזמן תקלה",
            "מראה נקי ומקצועי",
        ],
        "sales_script": (
            "נציג: היום יש לכם מצלמות מצוינות, אבל החיבורים והחשמל עדיין נקודת חולשה.\n"
            "אם נוסיף קופסאות חיבורים, מתאם קיר ו‑UPS קטן, גם בהפסקת חשמל המערכת ממשיכה להקליט "
            "וההתקנה נראית הרבה יותר מקצועית ללקוח שמגיע הביתה."
        ),
    },
    "ip_cam_4mp_pro": {
        "recommended": [
            "cam_mount_wall",
            "cam_pendant_mount",
            "poe_switch_16",
            "hdd_4tb",
            "ups_medium",
        ],
        "tagline": "מוכנות להתרחבות",
        "description": "שדרוג מערכת חכמה יותר עם יכולת להוספת מצלמות עתידיות.",
        "benefits": [
            "שיפור איכות כיסוי",
            "תמיכה בהרחבה עתידית",
            "מערכת יציבה למקצוענים",
        ],
        "sales_script": (
            "נציג: כבר השקעתם במצלמות החכמות. כדי לנצל אותן באמת, כדאי לעבור למתג PoE גדול יותר "
            "ולחזק את האחסון. כך תוכלו להוסיף מצלמות נוספות בלי עבודות נוספות בשטח, "
            "ולהיות מוכנים להתרחבות עתידית."
        ),
    },
    "turbohd_cam_2mp": {
        "recommended": [
            "cam_mount_wall",
            "cam_junction_box",
            "dvr_8ch_entry",
            "hdd_2tb",
            "ups_small",
        ],
        "tagline": "מערכת Turbo HD מלאה",
        "description": "הפיכת מצלמות בודדות למערכת Turbo HD שלמה עם אחסון וגיבוי.",
        "benefits": [
            "פתרון שלם ללקוח",
            "הקלטה רציפה",
            "העלאת ערך העסקה",
        ],
        "sales_script": (
            "נציג: כרגע יש לכם מצלמות בודדות. ברגע שנוסיף DVR, דיסק ו‑UPS קטן, "
            "זה כבר הופך למערכת Turbo HD מלאה – עם הקלטה מסודרת ויכולת לחזור לאירועים בזמן אמת."
        ),
    },
    "nvr_8ch_entry": {
        "recommended": [
            "hdd_2tb",
            "ups_small",
            "ip_cam_4mp_basic",
            "ip_cam_4mp_pro",
        ],
        "tagline": "מיצוי ערוצי NVR",
        "description": "הוספת מצלמות ואחסון כדי לנצל את כל הערוצים במערכת.",
        "benefits": [
            "כיסוי אזורים נוספים",
            "הגדלת סל המוצרים",
            "ערך גבוה ללקוח קיים",
        ],
        "sales_script": (
            "נציג: כרגע אתם מנצלים רק חלק קטן מה‑NVR. אם נוסיף עוד 2–3 מצלמות ודיסק 2TB, "
            "נכסה את כל האזורים שדיברנו עליהם וננצל את ההשקעה שכבר עשיתם במקום להשאיר ערוצים ריקים."
        ),
    },
    "nvr_16ch_pro": {
        "recommended": [
            "hdd_4tb",
            "ups_medium",
            "ip_cam_4mp_pro",
            "poe_switch_16",
        ],
        "tagline": "מערכת מקצועית מלאה",
        "description": "שדרוג אחסון ויציבות וניצול NVR מקצועי ליותר מצלמות.",
        "benefits": [
            "תמיכה בפרויקטים גדולים",
            "שיפור ביצועים",
            "אמינות גבוהה",
        ],
        "sales_script": (
            "נציג: זה NVR ברמה מקצועית, שמתאים גם להתרחבות עתידית. "
            "אם נוסיף דיסק 4TB, UPS בינוני ומתג 16 פורטים, "
            "תקבלו פלטפורמה יציבה שתתמוך בכם גם כשכמות המצלמות תגדל."
        ),
    },
    "dvr_8ch_entry": {
        "recommended": ["hdd_2tb", "ups_small", "turbohd_cam_2mp"],
        "tagline": "השלמת מערכת DVR",
        "description": "הוספת מצלמות לכל הערוצים ושיפור אחסון וגיבוי.",
        "benefits": [
            "כיסוי וידאו רחב",
            "שמירת אירועים קריטיים",
        ],
        "sales_script": (
            "נציג: ה‑DVR שלכם כבר מוכן לעד 8 מצלמות. "
            "אם נוסיף עוד מצלמות ודיסק 2TB יחד עם UPS, "
            "תהיו בטוחים שכל מה שקורה בעסק מתועד גם בזמן תקלות חשמל."
        ),
    },
    "access_ctrl_basic": {
        "recommended": ["door_lock_basic", "door_contact", "intercom_door_station"],
        "tagline": "גישה חכמה ומאובטחת",
        "description": "חיבור בקרת גישה לאינטרקום ומנעולים חכמים לכניסה מלאה.",
        "benefits": [
            "חוויית כניסה מודרנית",
            "שיפור אבטחה",
            "שילוב מערכת אחת ללקוח",
        ],
        "sales_script": (
            "נציג: היום יש לכם בקר גישה בסיסי. אם נוסיף מנעול חשמלי, מגנט דלת ואינטרקום וידאו, "
            "כל כניסה תתועד, תוכלו לראות מי בדלת ולתת גישה רק למי שמורשה – "
            "וזה גם נראה הרבה יותר מקצועי ללקוחות שמגיעים."
        ),
    },
    "door_lock_basic": {
        "recommended": ["door_contact", "intercom_door_station", "intercom_room_station"],
        "tagline": "שדרוג גישה קיימת",
        "description": "שדרוג מנעול קיים באמצעות חיווי דלת ואינטרקום וידאו.",
        "benefits": [
            "נוחות שימוש",
            "שיפור שליטה על כניסות",
        ],
        "sales_script": (
            "נציג: המנעול החשמלי כבר נותן שליטה, אבל בלי חיווי ואינטרקום לא באמת יודעים מה קורה בדלת. "
            "עם מגנט דלת ואינטרקום אתם גם רואים מי נכנס וגם יודעים אם הדלת באמת נסגרה."
        ),
    },
    "intercom_door_station": {
        "recommended": ["intercom_room_station", "access_ctrl_basic", "door_lock_basic"],
        "tagline": "פתרון כניסה מלא",
        "description": "שילוב אינטרקום עם בקרת גישה ונעילה חכמה.",
        "benefits": [
            "בקרה מרכזית על כניסות",
            "שדרוג חוויית אורחים",
        ],
        "sales_script": (
            "נציג: כרגע יש לכם אינטרקום בדלת. "
            "אם נחבר אותו לבקר הגישה ולמנעול החשמלי, "
            "תקבלו פתרון מלא – מזהים את מי שמגיע, פותחים מרחוק ומנהלים את כל הכניסות ממקום אחד."
        ),
    },
    "poe_switch_8": {
        "recommended": ["ip_cam_4mp_basic", "ip_cam_4mp_pro", "ups_small"],
        "tagline": "הרחבת מצלמות על גבי PoE",
        "description": "הוספת מצלמות מעל מתג קיים והגנה באמצעות UPS.",
        "benefits": [
            "ניצול תשתית קיימת",
            "הוספת כיסוי בקלות",
        ],
        "sales_script": (
            "נציג: כבר יש לכם מתג PoE, וזה מצוין. "
            "עם עוד 1–2 מצלמות ו‑UPS קטן נוכל לנצל את הפורטים הפנויים, "
            "להוסיף כיסוי ואזורים מתים בלי למשוך תשתית חדשה."
        ),
    },
    "poe_switch_16": {
        "recommended": ["ip_cam_4mp_pro", "ups_medium"],
        "tagline": "מתג מוכן לצמיחה",
        "description": "תמיכה במספר גדול של מצלמות למערכות מתרחבות.",
        "benefits": [
            "מוכנות לפרויקטים גדולים",
            "פחות ציוד מאולתר בשטח",
        ],
        "sales_script": (
            "נציג: אם יודעים שהמערכת הולכת לגדול, עדיף כבר עכשיו לעבור למתג 16 פורטים ו‑UPS מתאים. "
            "כך בכל פעם שתרצו להוסיף מצלמה נוספת – פשוט מחברים, בלי לשבור שוב תקרה וקירות."
        ),
    },
}



# -----------------------------
# Helper functions
# -----------------------------

def compute_customer_current_value(customer):
    total = 0
    for item in customer["installed"]:
        p = products.get(item["product_id"])
        if not p:
            continue
        total += item["count"] * p["list_price_estimate"]
    return total


def build_recommendation_packages(customer_id):
    customer = customers.get(customer_id)
    if not customer:
        return []

    # איסוף כל ה-triggerים מהמערכת הקיימת
    trigger_ids = {item["product_id"] for item in customer["installed"]}

    # מיפוי product_id -> מידע כלל-חבילה (tagline, benefits וכו')
    packages_by_trigger = {}
    for pid in trigger_ids:
        rule = cross_sell_rules.get(pid)
        if not rule:
            continue

        items = []
        total_price = 0
        for rid in rule["recommended"]:
            prod = products.get(rid)
            if not prod:
                continue
            price = prod["list_price_estimate"]
            items.append({
                "product_id": rid,
                "name": prod["name"],
                "price": price,
            })
            total_price += price

        if not items:
            continue

        packages_by_trigger[pid] = {
            "trigger_product_id": pid,
            "title": products.get(pid, {}).get("name", "חבילת הרחבה"),
            "tagline": rule.get("tagline", ""),
            "description": rule.get("description", ""),
            "benefits": rule.get("benefits", []),
            "sales_script": rule.get("sales_script", ""),
            "items": items,
            "totalPrice": total_price,
        }

    # כרגע – מחזירים חבילות נפרדות לכל trigger (כמו בדמו). אפשר לאחד בעתיד.
    return list(packages_by_trigger.values())


# -----------------------------
# Routes
# -----------------------------

@app.route("/")
def index():
    # ה-HTML מסתמך על JS שיקבל נתוני לקוח/המלצות ב-API
    return render_template("index.html")


@app.route("/api/customers")
def api_customers():
    # החזרה פשוטה של רשימת פרופילים (אם תרצה לטעון דינמית ל-UI בעתיד)
    resp = []
    for cid, c in customers.items():
        resp.append({
            "id": c["id"],
            "name": c["name"],
            "segment": c["segment"],
        })
    return jsonify({"customers": resp})


@app.route("/api/customer/<customer_id>")
def api_customer_detail(customer_id):
    c = customers.get(customer_id)
    if not c:
        return jsonify({"error": "customer_not_found"}), 404

    installed_detailed = []
    for item in c["installed"]:
        p = products.get(item["product_id"])
        if not p:
            continue
        installed_detailed.append({
            "product_id": p["id"],
            "name": p["name"],
            "count": item["count"],
            "unit_price": p["list_price_estimate"],
            "total_price": item["count"] * p["list_price_estimate"],
        })

    return jsonify({
        "id": c["id"],
        "name": c["name"],
        "segment": c["segment"],
        "installed": installed_detailed,
        "current_value": compute_customer_current_value(c),
    })


@app.route("/api/recommendations/<customer_id>")
def api_recommendations(customer_id):
    c = customers.get(customer_id)
    if not c:
        return jsonify({"error": "customer_not_found"}), 404

    packages = build_recommendation_packages(customer_id)
    return jsonify({
        "customer_id": customer_id,
        "packages": packages,
    })


if __name__ == "__main__":
    app.run(debug=True)
