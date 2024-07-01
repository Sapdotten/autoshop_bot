import asyncio
import os
<<<<<<< HEAD

from aiogram import Bot, Dispatcher
from bot.handlers import request
from aiogram.client.session.aiohttp import AiohttpSession
import logging

from load_env import load_environ

logging.basicConfig(level=logging.INFO)
def register_routers(dp):
    dp.include_routers(request.command_router)
=======
from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher


>>>>>>> 465acad (Start of developing)


async def main() -> None:
    """
    Entry point
    """
<<<<<<< HEAD
    # load_environ()
    
    session = AiohttpSession()
    bot = Bot(os.getenv("API_KEY"), session=session)
    dp = Dispatcher()
    register_routers(dp)
    request.regsier_bot(bot)
    try:
        await bot.delete_webhook()
        await dp.start_polling(bot)
    except Exception as ex:
        print(ex)
=======
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
>>>>>>> 465acad (Start of developing)


if __name__ == "__main__":
    asyncio.run(main())