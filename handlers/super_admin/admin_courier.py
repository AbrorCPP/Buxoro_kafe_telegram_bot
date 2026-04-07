from aiogram import F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from loader import db
from router import router
from config import S_ADMIN


class AddCourierState(StatesGroup):
    telegram_id = State()
    username = State()
    phone = State()


@router.message(Command("add_courier"), F.from_user.id.in_({int(S_ADMIN)}))
async def cmd_add_courier(message: Message, state: FSMContext):
    await state.set_state(AddCourierState.telegram_id)
    await message.answer("Yangi kuryerning Telegram ID sini kiriting:")


@router.message(AddCourierState.telegram_id)
async def process_courier_id(message: Message, state: FSMContext):
    tg_id = message.text.strip() if message.text else None
    if not tg_id or not tg_id.lstrip("-").isdigit():
        await message.answer("❌ Noto'g'ri format. Iltimos, faqat raqamli Telegram ID kiriting (masalan: 123456789):")
        return
    await state.update_data(telegram_id=tg_id)
    await state.set_state(AddCourierState.username)
    await message.answer("Kuryerning to'liq ismini kiriting:")


@router.message(AddCourierState.username)
async def process_courier_name(message: Message, state: FSMContext):
    name = message.text.strip() if message.text else None
    if not name:
        await message.answer("❌ Ism bo'sh bo'lishi mumkin emas. Qayta kiriting:")
        return
    await state.update_data(username=name)
    await state.set_state(AddCourierState.phone)

    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Kontaktni yuborish", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer(
        "Kuryerning telefon raqamini kiriting yoki kontaktni yuboring:",
        reply_markup=kb
    )


@router.message(AddCourierState.phone)
async def process_courier_phone(message: Message, state: FSMContext):
    # Contact button orqali yoki text orqali
    if message.contact:
        phone = message.contact.phone_number
    elif message.text:
        phone = message.text.strip()
        if not (phone.startswith("+") or phone.isdigit()):
            await message.answer("❌ Telefon raqami noto'g'ri. Masalan: +998901234567")
            return
    else:
        await message.answer("❌ Iltimos, telefon raqamini kiriting.")
        return

    data = await state.get_data()
    
    # Duplicate check
    existing = db.detect_courier(data['telegram_id'])
    if existing:
        await state.clear()
        await message.answer(
            f"⚠️ Bu Telegram ID bilan kuryer allaqachon mavjud: {existing['username']}",
            reply_markup=ReplyKeyboardRemove()
        )
        return
    
    db.add_courier(data['telegram_id'], data['username'], phone)
    await state.clear()
    await message.answer(
        f"✅ Kuryer muvaffaqiyatli qo'shildi!\n\n"
        f"👤 Ismi: {data['username']}\n"
        f"🆔 Telegram ID: {data['telegram_id']}\n"
        f"📞 Telefon: {phone}",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command("remove_courier"), F.from_user.id.in_({int(S_ADMIN)}))
async def cmd_remove_courier(message: Message):
    """Kuryerni o'chirish: /remove_courier <telegram_id>"""
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        couriers = db.get_all_couriers()
        if not couriers:
            await message.answer("Hozircha kuryerlar yo'q.")
            return
        text = "📋 Kuryerlar ro'yxati:\n\n"
        for c in couriers:
            text += f"👤 {c['username']} | 🆔 {c['telegram_id']} | 📞 {c['phone']}\n"
        text += "\n✂️ O'chirish uchun: /remove_courier <telegram_id>"
        await message.answer(text)
        return
    
    tg_id = args[1].strip()
    courier = db.detect_courier(tg_id)
    if not courier:
        await message.answer(f"❌ ID {tg_id} bilan kuryer topilmadi.")
        return
    
    db.delete_courier(tg_id)
    await message.answer(f"✅ Kuryer {courier['username']} o'chirildi.")


@router.message(Command("couriers"), F.from_user.id.in_({int(S_ADMIN)}))
async def cmd_list_couriers(message: Message):
    """Barcha kuryerlar ro'yxatini ko'rsatish"""
    couriers = db.get_all_couriers()
    if not couriers:
        await message.answer("Hozircha kuryerlar yo'q.\n\nQo'shish uchun: /add_courier")
        return
    text = "📋 Barcha kuryerlar:\n\n"
    for i, c in enumerate(couriers, 1):
        text += f"{i}. 👤 {c['username']} | 🆔 {c['telegram_id']} | 📞 {c['phone']}\n"
    await message.answer(text)
