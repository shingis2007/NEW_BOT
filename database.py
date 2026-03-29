import json
import os
from datetime import datetime

DB_FILE = "data/database.json"


def load_db():
    if not os.path.exists(DB_FILE):
        os.makedirs("data", exist_ok=True)
        default = {
            "users": {},
            "murojaatlar": [],
            "tadbirlar": [],
            "elanlar": [],
            "qatnashuvchilar": {},
            "kengash_azolari": []
        }
        save_db(default)
        return default
    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_db(data):
    os.makedirs("data", exist_ok=True)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def register_user(user_id, full_name, username):
    db = load_db()
    if str(user_id) not in db["users"]:
        db["users"][str(user_id)] = {
            "full_name": full_name,
            "username": username or "",
            "joined": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        save_db(db)


def get_all_users():
    db = load_db()
    return db["users"]


# ===== MUROJAATLAR =====

def add_murojaat(user_id, full_name, username, text):
    db = load_db()
    db["murojaatlar"].append({
        "id": len(db["murojaatlar"]) + 1,
        "user_id": user_id,
        "full_name": full_name,
        "username": username or "",
        "text": text,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status": "yangi"
    })
    save_db(db)


def get_murojaatlar():
    db = load_db()
    return db["murojaatlar"]


# ===== TADBIRLAR =====

def add_tadbir(nomi, sana, joy, tavsif):
    db = load_db()
    tadbir_id = len(db["tadbirlar"]) + 1
    db["tadbirlar"].append({
        "id": tadbir_id,
        "nomi": nomi,
        "sana": sana,
        "joy": joy,
        "tavsif": tavsif
    })
    save_db(db)
    return tadbir_id


def get_tadbirlar():
    db = load_db()
    return db["tadbirlar"]


def delete_tadbir(tadbir_id):
    db = load_db()
    db["tadbirlar"] = [t for t in db["tadbirlar"] if t["id"] != tadbir_id]
    save_db(db)


# ===== QATNASHUVCHILAR =====

def add_qatnashuvchi(tadbir_id, user_id, full_name, username, telefon=""):
    db = load_db()
    key = str(tadbir_id)
    if "qatnashuvchilar" not in db:
        db["qatnashuvchilar"] = {}
    if key not in db["qatnashuvchilar"]:
        db["qatnashuvchilar"][key] = []
    # Ikki marta ro'yxatdan o'tishni oldini olish
    for q in db["qatnashuvchilar"][key]:
        if q["user_id"] == user_id:
            return False
    db["qatnashuvchilar"][key].append({
        "user_id": user_id,
        "full_name": full_name,
        "username": username or "",
        "telefon": telefon,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    save_db(db)
    return True


def get_qatnashuvchilar(tadbir_id=None):
    db = load_db()
    if "qatnashuvchilar" not in db:
        return {} if not tadbir_id else []
    if tadbir_id:
        return db["qatnashuvchilar"].get(str(tadbir_id), [])
    return db["qatnashuvchilar"]


# ===== KENGASH A'ZOLARI =====

def add_kengash_azosi(ism, lavozim, username, photo_id=None):
    db = load_db()
    if "kengash_azolari" not in db:
        db["kengash_azolari"] = []
    db["kengash_azolari"].append({
        "id": len(db["kengash_azolari"]) + 1,
        "ism": ism,
        "lavozim": lavozim,
        "username": username or "",
        "photo_id": photo_id or "",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    save_db(db)


def get_kengash_azolari():
    db = load_db()
    return db.get("kengash_azolari", [])


def delete_kengash_azosi(azosi_id):
    db = load_db()
    db["kengash_azolari"] = [
        a for a in db.get("kengash_azolari", []) if a["id"] != azosi_id
    ]
    save_db(db)
