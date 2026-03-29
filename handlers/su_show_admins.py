from aiogram import Router,F
from aiogram.fsm.context import FSMContext
from keyboards import delete_admin
from aiogram.types import InlineKeyboardMarkup,CallbackQuery,Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from router import router
from loader import db,s_id

db = db

@router.message(lambda message: message.text == "/show_admins")
async def start_edit_handler(message: Message, state: FSMContext):
    if not str(message.from_user.id) == str(s_id):
        await message.answer("Siz Super_admin emassiz.🚫")
        return
    await state.clear()
    
    admins = db.execute("SELECT id, username FROM admin", fetchall=True)
    
    if not admins:
        return await message.answer("🤦‍♂️ Hozircha adminlar mavjud emas.")

    await message.answer(
        "👨‍💼 Mavjud adminlar:", 
        reply_markup=show_category_keyboard(admins)
    )
