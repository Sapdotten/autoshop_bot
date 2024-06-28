def check_phone_number(phone_number: str) -> bool:
    """Checks phone number

    Args:
        phone_number (str): phone number as str

    Returns:
        bool: True if number can be correct
    """
    return (
        len(phone_number) == 11
        or (
            len(phone_number) == 10
            and (phone_number[0] != "7" and phone_number[0] != "8")
        )
    ) and phone_number.isdigit()