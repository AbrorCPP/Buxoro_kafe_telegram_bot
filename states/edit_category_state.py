from aiogram.fsm.state import State, StatesGroup

class EditCategory(StatesGroup):
    waiting_for_select = State()  
    waiting_for_name = State()    
    waiting_for_image = State()   
    waiting_for_desc = State()     
