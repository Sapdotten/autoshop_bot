import asyncio
import os

from aiogram import Bot, Dispatcher
from bot.handlers import request
from aiogram.client.session.aiohttp import AiohttpSession
import logging

from load_env import load_environ

logging.basicConfig(level=logging.INFO)
def register_routers(dp):
    dp.include_routers(request.command_router)


async def main() -> None:
    """
    Entry point
    """
    # load_environ()
    token = os.getenv("API_KEY")
    
    session = AiohttpSession()
    bot = Bot(os.environ.get("API_KEY"), session=session)
    dp = Dispatcher()
    register_routers(dp)
    request.regsier_bot(bot)
    try:
        await bot.delete_webhook()
        await dp.start_polling(bot)
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    asyncio.run(main())