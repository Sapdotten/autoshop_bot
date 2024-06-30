from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import asyncio
from db_settings import DatabaseSettings
import logging
logging.basicConfig(level=logging.INFO)

user = 'tester'
password='12345678'
hostname = "localhost:5432"
dbname = 'tester'
# CONNECT_STRING = DatabaseSettings.get_url()

CONNECT_STRING = f"postgresql+asyncpg://{user}:{password}@{hostname}/{dbname}"

engine = create_async_engine(url=CONNECT_STRING, echo = False, max_overflow=10)

async def get_123():
    async with engine.connect() as conn:
        res = await conn.execute(text("SELECT VERSION()"))
        print(f"res={res.all()=}")
    
logging.info("Start")
asyncio.run(get_123())