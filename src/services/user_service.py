import re

from models.user import User


async def is_exist_by_phone(phone: str):
    if await is_phone(phone=phone):
        if await User.exists(phone=int(phone)):
            return True
    return False


async def is_phone(phone: str):
    if len(phone) == 11 and phone.startswith('7'):
        return True
    return False


async def is_exist_by_email(email: str):
    if await is_email(email=email):
        if await User.exists(email=email.lower()):
            return True
    return False

async def is_email(email: str):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email):
        return True
    return False