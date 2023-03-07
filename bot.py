import logging
import asyncio
from aiogram import Dispatcher, Bot, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from src.handlers import start, solve_tasks

logging.basicConfig(
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s %(levelname)s %(module)s.%(funcName)s: %(message)s",
)

# TODO: add storing token in environment
bot = Bot(token="6103736346:AAEG3okaRuEFXkpM_-KggQfRcNqWFDZN2JA", parse_mode=ParseMode.HTML)
# TODO: use redis FSM storage
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(start.router)
dp.include_router(solve_tasks.router)


@dp.startup()
async def add_commands():
    await bot.set_my_commands(
        [
            types.BotCommand(command="start", description="Начать общение с ботом"),
            types.BotCommand(command="start_solving", description="Перейти к выбору уровня"),
            types.BotCommand(command="get_result", description="Узнать количество полученных баллов и решённых задач"),
        ]
    )


asyncio.run(dp.start_polling(bot))
