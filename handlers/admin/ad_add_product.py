from aiogram import F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from router import router
from states.add_product_state import ProductAdd
from keyboards.inline.category_add_p import category_keyboard
from loader import db 

@router.message(F.text == "/add_product")
async def start_add_product(message: Message, state: FSMContext):
    categories = db.execute("SELECT id, name FROM categories", fetchall=True)
    kb = await category_keyboard(categories)
    await message.answer("Mahsulot qaysi kategoriyaga tegishli?", reply_markup=kb)
    await state.set_state(ProductAdd.waiting_for_category)

@router.callback_query(ProductAdd.waiting_for_category, F.data.startswith("cat_"))
async def process_category(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.split("_")[1])
    await state.update_data(category_id=category_id)
    await callback.message.edit_text("Mahsulot nomini kiriting:")
    await state.set_state(ProductAdd.waiting_for_name)
    await callback.answer()

@router.message(ProductAdd.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Tavsifni kiriting:")
    await state.set_state(ProductAdd.waiting_for_description)

@router.message(ProductAdd.waiting_for_description)
async def process_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Narxini kiriting:")
    await state.set_state(ProductAdd.waiting_for_price)

@router.message(ProductAdd.waiting_for_price)
async def process_price(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Raqam kiriting!")
    await state.update_data(price=int(message.text))
    await message.answer("📷 Rasm linkini yuboring:")
    await state.set_state(ProductAdd.waiting_for_photo)

@router.message(ProductAdd.waiting_for_photo, F.text)
async def process_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.text)
    data = await state.get_data()
    
    success = db.add_new_product(
        category_id=data['category_id'],
        name=data['name'],
        description=data['description'],
        price=data['price'],
        image_id=data['photo']
    )
    
    if success:
        await message.answer("✅ Mahsulot qo'shildi!")
    else:
        await message.answer("❌ Xatolik yuz berdi.")
        
    await state.clear()