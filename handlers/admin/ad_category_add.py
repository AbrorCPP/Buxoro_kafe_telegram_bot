#This file allows admins to enter categories using states;

from aiogram import types
from aiogram.fsm.context import FSMContext
from loader import db, bot
from router import router
from states.add_category_state import Category_creation_Form

db = db

@router.message(lambda message: message.text == "/add_category")
async def add_category_state(message: types.Message,state: FSMContext):
    name = db.detect_admin(message.from_user.id)
    if not name:
        await message.answer("Siz admin emassiz.🚫")
        return 
    sent_msg = await bot.send_message(message.chat.id, "Assalomu aleykum❗\n Qo'shmoqchi bo'lgan kategoriya nomini kiriting.🔽")
    await state.clear()
    await state.update_data(message_ids=[sent_msg.message_id])
    await state.set_state(Category_creation_Form.name)

@router.message(Category_creation_Form.name)
async def add_category_state_name(message: types.Message, state:FSMContext):
    await state.update_data(name = message.text)
    sent_msg = await bot.send_message(message.chat.id, "Kategoriya nomi qabul qilindi✅\nEndi kategoriya uchun tarifni yozing.🔽")
    data = await state.get_data()
    message_ids = data.get('message_ids', [])
    message_ids.append(sent_msg.message_id)
    await state.update_data(message_ids=message_ids)
    await state.set_state(Category_creation_Form.description)

@router.message(Category_creation_Form.description)
async def add_category_state_description(message: types.Message, state:FSMContext):
    await state.update_data(description = message.text)
    sent_msg = await bot.send_message(message.chat.id, "Kategoriya tarifi qabul qilindi.✅\nEndi category rasmi linkini jo'nating.🔽")
    data = await state.get_data()
    message_ids = data.get('message_ids', [])
    message_ids.append(sent_msg.message_id)
    await state.update_data(message_ids=message_ids)
    await state.set_state(Category_creation_Form.image_id)

@router.message(Category_creation_Form.image_id)
async def add_category_state_image_id(message: types.Message, state:FSMContext):
    await state.update_data(image_id = message.text)
    sent_msg = await bot.send_message(message.chat.id, "Rasm linki qabul qilindi.✅")
    data = await state.get_data()
    message_ids = data.get('message_ids', [])
    message_ids.append(sent_msg.message_id)
    await state.update_data(message_ids=message_ids)
    data = await state.get_data()
    try:
        db.category_creation(
            name = data['name'],
            image_id = data['image_id'],
            description = data['description']
            )
        success_msg = await bot.send_message(message.chat.id, "Muvaffaqiyatli ro'yxatga olindi✅")
        # Delete previous messages, keep success
        for msg_id in message_ids:
            try:
                await bot.delete_message(message.chat.id, msg_id)
            except Exception as e:
                print(f"Failed to delete message {msg_id}: {e}")
        await state.clear()
    except Exception as e:
        print(f"DB Error: {e}")
        error_msg = await bot.send_message(message.chat.id, "Ro'yxatga olishda bazada xatolik yuz berdi❌")
        # Delete previous, keep error
        for msg_id in message_ids:
            try:
                await bot.delete_message(message.chat.id, msg_id)
            except Exception as e:
                print(f"Failed to delete message {msg_id}: {e}")
        await state.clear()
