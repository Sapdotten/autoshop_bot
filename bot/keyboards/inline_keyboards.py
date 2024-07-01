from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_check_data_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Исправить имя", callback_data="change_name")],
            [
                InlineKeyboardButton(
                    text="Исправить телефон", callback_data="change_phone_number"
                )
            ],
            [InlineKeyboardButton(text="Исправить VIN", callback_data="change_vin")],
            [
                InlineKeyboardButton(
                    text="Исправить текст заявки", callback_data="change_text"
                )
            ],
            [InlineKeyboardButton(text="Все верно", callback_data="checks_passed")],
        ]
    )
