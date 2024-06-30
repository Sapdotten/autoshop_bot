from aiogram.fsm.state import State, StatesGroup

class UserFormState(StatesGroup):
    FIO = State()
    VIN = State()
    PHONE_NUMBER = State()
    PROBLEM = State()
    