from aiogram import Router,F
from aiogram.fsm.context import FSMContext
from keyboards.inline.edit_category import edit_category_keyboard
from states.edit_category_state import EditCategory
from aiogram.types import InlineKeyboardMarkup,CallbackQuery,Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from router import router
from loader import db

db = db

@router.message(lambda message: message.text == "/edit_category")
async def start_edit_handler(message: Message, state: FSMContext):
    name = db.detect_admin(message.from_user.id)
    if not name:
        await message.answer("Siz admin emassiz.🚫")
        return 
    
    categories = db.execute("SELECT id, name FROM categories", fetchall=True)
    
    if not categories:
        return await message.answer("Hozircha kategoriyalar mavjud emas.")

    await message.answer(
        "Tahrirlash uchun kategoriyani tanlang:", 
        reply_markup=edit_category_keyboard(categories)
    )
    await state.set_state(EditCategory.waiting_for_select)


@router.callback_query(EditCategory.waiting_for_select, F.data.startswith("edit_all_"))
async def process_category_selection(callback: CallbackQuery, state: FSMContext):
    cat_id = int(callback.data.split("_")[2])
    await state.update_data(cat_id=cat_id) 
    
    await callback.message.answer("1. Kategoriya uchun yangi **NOM** kiriting: 🔽")
    await state.set_state(EditCategory.waiting_for_name)
    await callback.answer()

@router.message(EditCategory.waiting_for_name)
async def get_new_name(message: Message, state: FSMContext):
    await state.update_data(new_name=message.text)
    await message.answer("2. Endi yangi **RASM** yuklang (photo yuboring): 🔽")
    await state.set_state(EditCategory.waiting_for_image)

@router.message(EditCategory.waiting_for_image, F.photo)
async def get_new_image(message: Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id        
    await state.update_data(new_image_id=photo_file_id)
    await message.answer("3. Oxirgi qadam: Yangi **TAVSIF** (description) kiriting:")
    await state.set_state(EditCategory.waiting_for_desc)

@router.message(EditCategory.waiting_for_desc)
async def finalize_category_edit(message: Message, state: FSMContext):
    new_description = message.text
    data = await state.get_data()
    
    cat_id = data['cat_id']
    name = data['new_name']
    image_id = data['new_image_id']
    sql = "UPDATE categories SET name=%s, image_id=%s, description=%s WHERE id=%s"
    params = (name, image_id, new_description, cat_id)
    
    try:
        db.execute(sql, params, commit=True)
        await message.answer(f"✅ **{name}** kategoriyasi muvaffaqiyatli yangilandi!")
    except Exception as e:
        await message.answer(f"⚠️ Xatolik yuz berdi: {e}")
    
    await state.clear()