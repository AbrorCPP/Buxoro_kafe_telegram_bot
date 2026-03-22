from aiogram.fsm.state import State, StatesGroup

class UserRegistrationForm(StatesGroup):
    fullname = State()
    phone = State()
    address = State()