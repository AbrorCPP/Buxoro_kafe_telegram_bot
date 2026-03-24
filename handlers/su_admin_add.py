#This form allows super_user in

from aiogram import types
from aiogram.fsm.context import FSMContext
from loader import s_id, db
from router import router
from states.add_admin_state import AdminRegistrationForm

db = db

@router.message(lambda message: message.text == "/add_admin")
async def add_admin(message: types.Message, state: FSMContext):
    if not str(message.from_user.id) == str(s_id):
        await message.answer("Siz Super_admin emassiz.🚫")
        return
    await state.clear()
    await message.answer(text="Adminning ism familiyasini kiriting:")
    await state.set_state(AdminRegistrationForm.username)


@router.message(AdminRegistrationForm.username)
async def add_admin_username(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer("Admin ism familiyasi qabul qilindi✅\nAdmin telegram_id sini kiriting⬇️")
    await state.set_state(AdminRegistrationForm.telegram_id)


@router.message(AdminRegistrationForm.telegram_id)
async def add_admin_telegram_id(message: types.Message, state: FSMContext):
    if message.text and message.text.isdigit():
        await state.update_data(telegram_id=message.text)
        await message.answer("Admin telegram idsi qabul qilindi✅\nTelefon raqamini kiriting⬇️")
        await state.set_state(AdminRegistrationForm.phone)
    else:
        await message.answer("Xato format❌ Faqat raqamlardan iborat bo'lishi kerak.")


@router.message(AdminRegistrationForm.phone)
async def add_admin_phone(message: types.Message, state: FSMContext):
    if message.text and (message.text.isdigit() or message.text.startswith('+')):
        await state.update_data(phone=message.text)
        data = await state.get_data()

        try:
            # DB metodiga ma'lumotlarni yuboramiz
            db.add_admin(
                data["telegram_id"],
                data["username"],
                data["phone"]
            )
            await message.answer("Muvaffaqiyatli ro'yxatga olindi✅")
            await state.clear()  # Jarayon tugadi, holatni tozalaymiz
        except Exception as e:
            print(f"DB Error: {e}")
            await message.answer("Ro'yxatga olishda bazada xatolik yuz berdi❌")
            await state.clear()
    else:
        await message.answer(text="Telefon raqam noto'g'ri formatda❌")