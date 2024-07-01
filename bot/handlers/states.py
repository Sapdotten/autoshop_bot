from aiogram.fsm.state import State, StatesGroup


class UserFormState(StatesGroup):
    FIO = State()
    VIN = State()
    PHONE_NUMBER = State()
    PROBLEM = State()
    CHECK = State()
    AUTO = State()
    EDIT_AUTO = State()
    CHANGE_FIO = State()
    CHANGE_PHONE_NUMBER = State()
    CHANGE_VIN = State()
    CHANGE_PROBLEM = State()
