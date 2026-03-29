from aiogram import types,F
from aiogram.types import message
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loader import s_id, db
from router import router
from states.add_admin_state import AdminRegistrationForm
from keyboards.inline.delete_admin_keyboard import delete_admin_keyboard

db = db

@router.message(lambda message: message.text == "/delete_admin")
async def add_admin(message: types.Message, state: FSMContext):
    if not str(message.from_user.id) == str(s_id):
        await message.answer("Siz Super_admin emassiz.🚫")
        return
    await state.clear()
    
    admins = db.get_all_admins()

    await message.answer(
        "Barcha adminlar ro'yxati",
        reply_markup=delete_admin_keyboard(admins))
    

@router.callback_query(F.data.startswith("delete_ad_"))
async def process_category_selection(callback: CallbackQuery, state: FSMContext):
    cat_id = int(callback.data.split("_")[2])
    
    try:
        db.delete_admin(cat_id)
        await callback.message.answer("✅ Successfully deleted.")
        await callback.answer()
    except Exception as e:
        print(f"O'chirishda xatolik: {e}")
        await callback.message.answer(f"⚠️ Xatolik: {e}")