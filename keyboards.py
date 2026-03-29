from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)


def user_main_menu():
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📢 E'lonlar"), KeyboardButton(text="📅 Tadbirlar")],
        [KeyboardButton(text="📨 Murojaat"), KeyboardButton(text="👥 Kengash a'zolari")],
        [KeyboardButton(text="ℹ️ Biz haqimizda")]
    ], resize_keyboard=True)
    return kb


def admin_main_menu():
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📤 E'lon yuborish"), KeyboardButton(text="📅 Tadbir qo'shish")],
        [KeyboardButton(text="📨 Murojaatlar"), KeyboardButton(text="🙋 Qatnashuvchilar")],
        [KeyboardButton(text="➕ Kengash a'zosi qo'shish"), KeyboardButton(text="🗑 A'zoni o'chirish")],
        [KeyboardButton(text="👥 Foydalanuvchilar"), KeyboardButton(text="🔙 Foydalanuvchi menyusi")]
    ], resize_keyboard=True)
    return kb


def cancel_kb():
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="❌ Bekor qilish")]
    ], resize_keyboard=True)
    return kb


def telefon_kb():
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📱 Raqamni yuborish", request_contact=True)],
        [KeyboardButton(text="❌ Bekor qilish")]
    ], resize_keyboard=True)
    return kb


def qatnashish_kb(tadbir_id):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Men qatnashaman", callback_data=f"qatnash_{tadbir_id}")]
    ])
    return kb
