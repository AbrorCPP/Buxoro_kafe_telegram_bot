#This file allows admins to enter categories using states;

from aiogram import types
from aiogram.fsm.context import FSMContext
from loader import db
from router import router
from states.add_category_state import Category_creation_Form

db = db

@router.message(lambda message: message.text == "/add_category")
async def add_category_state(message: types.Message,state: FSMContext):
    name = db.detect_admin(message.from_user.id)
    if not name:
        await message.answer("Siz admin emassiz.🚫")
        return 
    await message.answer("Assalomu aleykum❗\n Qo'shmoqchi bo'lgan kategoriya nomini kiriting.🔽")
    await state.clear()
    await state.set_state(Category_creation_Form.name)

@router.message(Category_creation_Form.name)
async def add_category_state_name(message: types.Message, state:FSMContext):
    await state.update_data(name = message.text)
    await message.answer("Kategoriya nomi qabul qilindi✅\nEndi kategoriya uchun tarifni yozing.🔽")
    await state.set_state(Category_creation_Form.description)

@router.message(Category_creation_Form.description)
async def add_category_state_description(message: types.Message, state:FSMContext):
    await state.update_data(description = message.text)
    await message.answer("Kategoriya tarifi qabul qilindi.✅\nEndi category rasmi linkini jo'nating.🔽")
    await state.set_state(Category_creation_Form.image_id)

@router.message(Category_creation_Form.image_id)
async def add_category_state_image_id(message: types.Message, state:FSMContext):
    await state.update_data(image_id = message.text)
    await message.answer("Rasm linki qabul qilindi.✅")
    data = await state.get_data()
    try:
        db.category_creation(
            name = data['name'],
            image_id = data('image_id'),
            description = data('description'),
            )
        await message.answer("Muvaffaqiyatli ro'yxatga olindi✅")
        await state.clear()
    except Exception as e:
        print(f"DB Error: {e}")
        await message.answer("Ro'yxatga olishda bazada xatolik yuz berdi❌")
        await state.clear()
