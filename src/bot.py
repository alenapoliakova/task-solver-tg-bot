import logging
import asyncio
from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from src.handlers import start, solve_tasks

logging.basicConfig(level=logging.DEBUG)

# TODO: add storing token in environment
bot = Bot(token="6103736346:AAEG3okaRuEFXkpM_-KggQfRcNqWFDZN2JA", parse_mode=ParseMode.HTML)
# TODO: use redis FSM storage
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(start.router)
dp.include_router(solve_tasks.router)

asyncio.run(dp.start_polling(bot))
