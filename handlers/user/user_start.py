from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from keyboards.reply.main_menu import main_menu_inline

from router import router
from states.start_state import UserRegistrationForm
from loader import db

db = db

WELCOME_NEW = (
    "👋 <b>Assalomu alaykum!</b>\n\n"
    "🍽 <b>Buxoro Kafe</b> botiga xush kelibsiz!\n"
    "━━━━━━━━━━━━━━━━━\n"
    "Davom etish uchun ro'yxatdan o'ting.\n\n"
    "✏️ To'liq ismingizni kiriting:"
)

def welcome_back(username: str) -> str:
    return (
        f"👋 <b>Xush kelibsiz, {username}!</b>\n\n"
        f"🏪 <b>Buxoro Kafe</b> — mazali taomlar yetkazib berish\n"
        f"━━━━━━━━━━━━━━━━━\n"
        f"🍜 Yangi buyurtma berish uchun menyuni oching\n"
        f"📦 Buyurtmalaringiz holatini kuzating\n\n"
        f"<i>Kerakli bo'limni tanlang 👇</i>"
    )

@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    try:
        user = db.detect_user(str(telegram_id))
    except Exception as e:
        print(f"Detect user error: {e}")
        user = None

    if not user:
        await state.clear()
        await message.answer(WELCOME_NEW, parse_mode="HTML")
        await state.set_state(UserRegistrationForm.fullname)
    else:
        name = user.get('username') or message.from_user.first_name or 'Mehmon'
        await message.answer(
            welcome_back(name),
            reply_markup=main_menu_inline(),
            parse_mode="HTML"
        )

@router.message(UserRegistrationForm.fullname)
async def process_fullname(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await state.set_state(UserRegistrationForm.phone)
    await message.answer(
        "✅ Ajoyib!\n\n"
        "📱 Endi telefon raqamingizni yuboring:\n"
        "<i>Masalan: +998901234567</i>",
        parse_mode="HTML"
    )

@router.message(UserRegistrationForm.phone)
async def process_phone(message: Message, state: FSMContext):
    if message.text and (message.text.isdigit() or message.text.startswith('+')):
        await state.update_data(phone=message.text)

        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="📍 Joylashuvni yuborish", request_location=True)]],
            resize_keyboard=True,
            one_time_keyboard=True
        )

        await state.set_state(UserRegistrationForm.address)
        await message.answer(
            "📍 <b>Oxirgi qadam!</b>\n\n"
            "Pastdagi tugma orqali joylashuvingizni yuboring.\n"
            "<i>Bu yetkazib berish narxini hisoblash uchun kerak.</i>",
            reply_markup=kb,
            parse_mode="HTML"
        )
    else:
        await message.answer(
            "❌ <b>Noto'g'ri format!</b>\n\n"
            "Iltimos, telefon raqamingizni to'g'ri kiriting.\n"
            "<i>Masalan: +998901234567</i>",
            parse_mode="HTML"
        )

@router.message(UserRegistrationForm.address, F.location)
async def process_address(message: Message, state: FSMContext):
    coordinates = f"{message.location.latitude}, {message.location.longitude}"
    data = await state.get_data()

    try:
        db.user_registration(
            username=str(data.get("fullname")),
            telegram_id=str(message.from_user.id),
            phone=str(data.get("phone")),
            coordinates=coordinates,
        )
        name = data.get("fullname") or message.from_user.first_name
        await message.answer(
            f"🎉 <b>Ro'yxatdan o'tish yakunlandi!</b>\n\n"
            f"👋 Xush kelibsiz, <b>{name}</b>!\n"
            f"━━━━━━━━━━━━━━━━━\n"
            f"🍽 Buxoro Kafe menyusidan buyurtma bering\n"
            f"🚀 Tez yetkazib beramiz!\n\n"
            f"<i>Kerakli bo'limni tanlang 👇</i>",
            reply_markup=main_menu_inline(),
            parse_mode="HTML"
        )
        await state.clear()

    except Exception as e:
        print(f"Registration error: {e}")
        await message.answer(
            "❌ Ro'yxatdan o'tishda xatolik yuz berdi!\n"
            "Iltimos, /start orqali qayta urinib ko'ring.",
            parse_mode="HTML"
        )