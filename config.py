import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN muhit o'zgaruvchisi o'rnatilmagan!")

ADMIN_IDS = []
admin_id = os.environ.get("ADMIN_ID", "")
if admin_id:
    try:
        ADMIN_IDS = [int(x.strip()) for x in admin_id.split(",") if x.strip()]
    except ValueError:
        pass

DB_FILE = "data/database.json"
