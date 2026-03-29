from aiogram import Router,F
from aiogram.fsm.context import FSMContext
from keyboards.inline.show_category import show_category_keyboard
from aiogram.types import InlineKeyboardMarkup,CallbackQuery,Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from router import router
from loader import db

db = db

@router.message(lambda message: message.text == "/show_category")
async def start_edit_handler(message: Message, state: FSMContext):
    name = db.detect_admin(message.from_user.id)
    if not name:
        await message.answer("Siz admin emassiz.🚫")
        return
    
    categories = db.execute("SELECT id, name FROM categories", fetchall=True)
    
    if not categories:
        return await message.answer("Hozircha kategoriyalar mavjud emas.")

    await message.answer(
        "🍽️ Mavjud kategoriyalar:", 
        reply_markup=show_category_keyboard(categories)
    )
