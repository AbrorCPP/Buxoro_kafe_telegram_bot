from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from keyboards.reply.main_menu import main_menu_inline

from router import router
from states.start_state import UserRegistrationForm
from loader import db

db = db

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
        await message.answer(
            "Assalomu alaykum! 😊\nBotdan foydalanish uchun ro'yxatdan o'ting.\n\nTo'liq ismingizni kiriting:")
        await state.set_state(UserRegistrationForm.fullname)
    else:
        name = user.get('username', 'Foydalanuvchi')
        text = (
            f"\n<b>Assalomu alaykum, {message.from_user.username}!</b> 👋\n\n"
            f"🤖 <b>Buxoro Kafe</b> botiga xush kelibsiz.\n"
            f"Siz bu yerda eng mazali taomlarni topishingiz mumkin.\n\n"
            f"<i>Kerakli bo'limni tanlang:</i>"
        )
        await message.answer(
            text = text,
            reply_markup=main_menu_inline(),
            parse_mode="HTML"
            )

@router.message(UserRegistrationForm.fullname)
async def process_fullname(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await state.set_state(UserRegistrationForm.phone)
    await message.answer("Rahmat! Endi telefon raqamingizni yuboring:")

@router.message(UserRegistrationForm.phone)
async def process_phone(message: Message, state: FSMContext):
    if message.text and (message.text.isdigit() or message.text.startswith('+')):
        await state.update_data(phone=message.text)

        kb = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Joylashuvni yuborish 📍", request_location=True)]],
            resize_keyboard=True,
            one_time_keyboard=True
        )

        await state.set_state(UserRegistrationForm.address)
        await message.answer("Oxirgi qadam: pastdagi tugma orqali joylashuvingizni yuboring!", reply_markup=kb)
    else:
        await message.answer("Iltimos, telefon raqamingizni to'g'ri kiriting (masalan: +998901234567):")

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
        text = (
            f"\n<b>Assalomu alaykum, {message.from_user.username}!</b> 👋\n\n"
            f"🤖 <b>Buxoro Kafe</b> botiga xush kelibsiz.\n"
            f"Siz bu yerda eng mazali taomlarni topishingiz mumkin.\n\n"
            f"<i>Kerakli bo'limni tanlang:</i>"
        )
        await message.answer(
            text = "Ro'yxatdan o'tish muvaffaqiyatli yakunlandi! ✅" + text,
            reply_markup=main_menu_inline(),
            parse_mode="HTML"
        )
        await state.clear()

    except Exception as e:
        print(f"Registration error: {e}");
        await message.answer("Ro'yxatdan o'tishda xatolik yuz berdi!")