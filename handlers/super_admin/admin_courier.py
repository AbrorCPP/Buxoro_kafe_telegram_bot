from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from loader import db
from router import router
from config import S_ADMIN

class AddCourierState(StatesGroup):
    telegram_id = State()
    username = State()
    phone = State()

@router.message(Command("add_courier"), F.from_user.id.in_({int(S_ADMIN)}))
async def cmd_add_courier(message: Message, state: FSMContext):
    await state.set_state(AddCourierState.telegram_id)
    await message.answer("Yangi kuryerning Telegram ID sini kiriting:")

@router.message(AddCourierState.telegram_id)
async def process_courier_id(message: Message, state: FSMContext):
    await state.update_data(telegram_id=message.text)
    await state.set_state(AddCourierState.username)
    await message.answer("Kuryerning ismini kiriting:")

@router.message(AddCourierState.username)
async def process_courier_name(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(AddCourierState.phone)
    await message.answer("Kuryerning telefon raqamini kiriting:")

@router.message(AddCourierState.phone)
async def process_courier_phone(message: Message, state: FSMContext):
    data = await state.get_data()
    db.add_courier(data['telegram_id'], data['username'], message.text)
    await state.clear()
    await message.answer(f"Kuryer muvaffaqiyatli qo'shildi: {data['username']}")
