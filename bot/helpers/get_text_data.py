from aiogram import types
def get_text_from_data(data: dict, callback: types.CallbackQuery = None) -> str:
    """Translatees data from dict to str for message

    Args:
        data (dict): data from UserFormState
        callback (types.CallbackQuery): callabck object from inline keyboard

    Returns:
        str: _description_
    """
    if callback:
        answer = f"""Имя: {data['FIO']}
tg: @{callback.from_user.username}
Номер телефона: {data['PHONE_NUMBER']}
VIN: {data['VIN']}\n
Заявка: {data['PROBLEM']}"""
    else:
        answer = f"""Имя: {data['FIO']}
Номер телефона: {data['PHONE_NUMBER']}
VIN: {data['VIN']}
Заявка: {data['PROBLEM']}"""
    return answer