from aiogram.fsm.state import State, StatesGroup

class AdminRegistrationForm(StatesGroup):
    telegram_id = State()
    username = State()
    phone = State()

