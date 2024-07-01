from aiogram import types
def get_text_from_data(data: dict, callback: types.CallbackQuery = None) -> str:
    """Translatees data from dict to str for message

    Args:
        data (dict): data from UserFormState
        callback (types.CallbackQuery): callabck object from inline keyboard

    Returns:
        str: _description_
    """
    name = f"Имя: {data['FIO']}\n"
    phone = f"Номер телефона: {data['PHONE_NUMBER']}\n"
    tg = ""
    vin = f"VIN: {data['VIN']}\n"
    car_name = ""
    request = f"Заявка: {data['PROBLEM']}"
    
    if data['VIN'] == "отсутствует":
        car_name = f"Модель машины: {data['AUTO']}"
    
    if callback:
        tg =  f"tg: @{callback.from_user.username}\n"

    return name+phone+tg+vin+car_name+'\n'+request
