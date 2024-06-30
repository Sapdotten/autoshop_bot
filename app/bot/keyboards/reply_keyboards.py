from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Returns keyboard for make reuest

    Returns:
        ReplyKeyboardMarkup:  keyboard
    """
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Сделать заказ')]
    ], resize_keyboard=True, one_time_keyboard=True)