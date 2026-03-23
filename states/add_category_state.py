from aiogram.fsm.state import State, StatesGroup

class Category_creation_Form(StatesGroup):
    name=State()
    image_id=State()
    description=State()

