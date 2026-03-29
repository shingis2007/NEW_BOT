from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards import user_main_menu, cancel_kb, qatnashish_kb, telefon_kb
from database import register_user, add_murojaat, get_tadbirlar, add_qatnashuvchi, get_kengash_azolari
from config import ADMIN_IDS

router = Router()


# ===== STATES =====

class MurojaatState(StatesGroup):
    text = State()


class QatnashState(StatesGroup):
    tadbir_id = State()
    ism = State()
    telefon = State()


# ===== /start =====

@router.message(CommandStart())
async def start(message: Message):
    register_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    await message.answer(
        f"👋 Assalomu alaykum, <b>{message.from_user.full_name}</b>!\n\n"
        "🎓 <b>Universitetdagi Yoshlar Ittifoqi</b> botiga xush kelibsiz!\n\n"
        "Quyidagi xizmatlardan foydalanishingiz mumkin:",
        reply_markup=user_main_menu(),
        parse_mode="HTML"
    )


# ===== E'LONLAR =====

@router.message(F.text == "📢 E'lonlar")
async def elanlar(message: Message):
    await message.answer(
        "📢 <b>So'nggi e'lonlar</b>\n\nHozircha yangi e'lon yo'q. Kuzatib boring!",
        parse_mode="HTML"
    )


# ===== TADBIRLAR =====

@router.message(F.text == "📅 Tadbirlar")
async def tadbirlar(message: Message):
    tadbirlar_list = get_tadbirlar()
    if not tadbirlar_list:
        await message.answer("📅 Hozircha rejalashtirilgan tadbir yo'q.")
        return
    for t in tadbirlar_list:
        text = (
            f"📅 <b>{t['nomi']}</b>\n"
            f"📆 Sana: {t['sana']}\n"
            f"📍 Joy: {t['joy']}\n"
            f"📝 {t['tavsif']}"
        )
        await message.answer(text, reply_markup=qatnashish_kb(t['id']), parse_mode="HTML")


# ===== QATNASHISH =====

@router.callback_query(F.data.startswith("qatnash_"))
async def qatnash_start(callback: CallbackQuery, state: FSMContext):
    tadbir_id = int(callback.data.split("_")[1])
    await state.set_state(QatnashState.ism)
    await state.update_data(tadbir_id=tadbir_id)
    await callback.message.answer(
        "👤 Ism-familiyangizni kiriting:\n(Masalan: Alisher Karimov)",
        reply_markup=cancel_kb()
    )
    await callback.answer()


@router.message(QatnashState.ism)
async def qatnash_ism(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Bekor qilindi.", reply_markup=user_main_menu())
        return
    await state.update_data(ism=message.text)
    await state.set_state(QatnashState.telefon)
    await message.answer(
        "📱 Telefon raqamingizni kiriting:",
        reply_markup=telefon_kb()
    )


@router.message(QatnashState.telefon)
async def qatnash_telefon(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Bekor qilindi.", reply_markup=user_main_menu())
        return

    if message.contact:
        telefon = message.contact.phone_number
    elif message.text:
        telefon = message.text
    else:
        await message.answer("📱 Iltimos telefon raqam yuboring:")
        return

    data = await state.get_data()
    tadbir_id = data["tadbir_id"]
    ism = data["ism"]
    user = message.from_user

    tadbirlar = get_tadbirlar()
    tadbir = next((t for t in tadbirlar if t['id'] == tadbir_id), None)
    tadbir_nomi = tadbir['nomi'] if tadbir else f"#{tadbir_id}"

    natija = add_qatnashuvchi(tadbir_id, user.id, ism, user.username, telefon)
    await state.clear()

    if natija:
        await message.answer(
            f"✅ <b>Muvaffaqiyatli ro'yxatdan o'tdingiz!</b>\n\n"
            f"📅 Tadbir: <b>{tadbir_nomi}</b>\n"
            f"👤 Ism: {ism}\n"
            f"📱 Telefon: {telefon}\n\n"
            f"Tadbir haqida xabar beramiz!",
            reply_markup=user_main_menu(),
            parse_mode="HTML"
        )
        for admin_id in ADMIN_IDS:
            try:
                await message.bot.send_message(
                    admin_id,
                    f"🙋 <b>Yangi qatnashuvchi!</b>\n\n"
                    f"📅 Tadbir: <b>{tadbir_nomi}</b>\n"
                    f"👤 Ism: {ism}\n"
                    f"📱 Telefon: {telefon}\n"
                    f"🔗 Nickname: @{user.username or 'username yoq'}\n"
                    f"🆔 ID: <code>{user.id}</code>",
                    parse_mode="HTML"
                )
            except Exception:
                pass
    else:
        await message.answer(
            "ℹ️ Siz allaqachon ro'yxatga olindingiz!",
            reply_markup=user_main_menu()
        )


# ===== MUROJAAT =====

@router.message(F.text == "📨 Murojaat")
async def murojaat_start(message: Message, state: FSMContext):
    await state.set_state(MurojaatState.text)
    await message.answer(
        "📨 <b>Murojaat yuborish</b>\n\n"
        "Ariza, savol yoki muammoingizni yozing.\n"
        "Tez orada javob beramiz!",
        reply_markup=cancel_kb(),
        parse_mode="HTML"
    )


@router.message(MurojaatState.text)
async def murojaat_save(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("Bekor qilindi.", reply_markup=user_main_menu())
        return

    add_murojaat(
        message.from_user.id,
        message.from_user.full_name,
        message.from_user.username,
        message.text
    )

    for admin_id in ADMIN_IDS:
        try:
            await message.bot.send_message(
                admin_id,
                f"📨 <b>Yangi murojaat!</b>\n\n"
                f"👤 Kim: {message.from_user.full_name}\n"
                f"🔗 Nickname: @{message.from_user.username or 'username yoq'}\n"
                f"🆔 ID: <code>{message.from_user.id}</code>\n\n"
                f"💬 Murojaat:\n{message.text}\n\n"
                f"📨 Javob berish: /javob_{message.from_user.id}",
                parse_mode="HTML"
            )
        except Exception:
            pass

    await state.clear()
    await message.answer(
        "✅ Murojaatingiz qabul qilindi!\n24 soat ichida javob beramiz.",
        reply_markup=user_main_menu()
    )


# ===== KENGASH A'ZOLARI =====

@router.message(F.text == "👥 Kengash a'zolari")
async def kengash(message: Message):
    azolar = get_kengash_azolari()
    if not azolar:
        await message.answer(
            "👥 <b>Kengash a'zolari</b>\n\nHozircha ma'lumot kiritilmagan.",
            parse_mode="HTML"
        )
        return
    await message.answer("👥 <b>Yoshlar Ittifoqi Kengash A'zolari</b>", parse_mode="HTML")
    for a in azolar:
        text = (
            f"💼 <b>{a['lavozim']}</b>\n"
            f"👤 {a['ism']}\n"
            f"🔗 {a['username']}"
        )
        if a.get('photo_id'):
            await message.answer_photo(photo=a['photo_id'], caption=text, parse_mode="HTML")
        else:
            await message.answer(text, parse_mode="HTML")


# ===== BIZ HAQIMIZDA =====

@router.message(F.text == "ℹ️ Biz haqimizda")
async def haqimizda(message: Message):
    await message.answer(
        "🎓 <b>Yoshlar Ittifoqi haqida</b>\n\n"
        "Biz universiteti talabalari hayotini yanada mazmunli qilish uchun ishlaydi.\n\n"
        "🎯 Maqsadimiz: Yoshlarni birlashtirish, rivojlantirish va qo'llab-quvvatlash.\n\n"
        "📞 Bog'lanish: @yoshlar_admin",
        parse_mode="HTML"
    )
