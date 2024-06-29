from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import asyncio

user = 'tester'
password='12345678'
hostname = "localhost:5432"
dbname = 'tester'
CONNECT_STRING = f"postgresql+asyncpg://{user}:{password}@{hostname}/{dbname}"

engine = create_async_engine(url=CONNECT_STRING, echo = False, max_overflow=10)

async def get_123():
    async with engine.connect() as conn:
        res = await conn.execute(text("SELECT VERSION()"))
        print(f"res={res.all()}")
    
asyncio.run(get_123())