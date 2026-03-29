from aiogram import Router,F
from aiogram.fsm.context import FSMContext
from keyboards.inline.delete_category import delete_category_keyboard
from aiogram.types import InlineKeyboardMarkup,CallbackQuery,Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from router import router
from loader import db


db = db

@router.message(lambda message: message.text == "/delete_category") 
async def show_categories_for_delete(message: Message):
    if not db.detect_admin(message.from_user.id):
        return await message.answer("Siz admin emassiz.🚫")

    categories = db.execute("SELECT id, name FROM categories", fetchall=True)
    
    if not categories:
        return await message.answer("Hozircha kategoriyalar mavjud emas.")

    await message.answer(
        "🚫 O'chirish uchun kategoriyani tanlang:", 
        reply_markup=delete_category_keyboard(categories) 
    )

@router.callback_query(F.data.startswith("del_cat_")) 
async def process_delete_category(callback: CallbackQuery):
    cat_id = int(callback.data.split("_")[2])

    try:
        db.delete_category(cat_id)
        await callback.answer("Kategoriya o'chirildi!", show_alert=True)
        await callback.message.edit_text("Kategoriya muvaffaqiyatli o'chirildi. ✅")
    except Exception as e:
        print(f"Xatolik: {e}")
        await callback.answer("⚠️ O'chirishda xatolik yuz berdi.", show_alert=True)