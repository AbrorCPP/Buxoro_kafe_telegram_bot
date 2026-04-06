from aiogram.fsm.state import StatesGroup, State

class CheckoutState(StatesGroup):
    location = State()
