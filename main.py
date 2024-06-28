import asyncio
import os
from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher




async def main() -> None:
    """
    Entry point
    """
    load_dotenv('.env')
    token = os.environ.het("API_KEY")
    bot = Bot(token)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    try:
        await dp.skip_updates()
        await dp.start_polling()
    except Exception as _ex:
        print(_ex)


if __name__ == "__main__":
    asyncio.run(main())