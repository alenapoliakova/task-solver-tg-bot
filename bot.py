import logging
import asyncio
from aiogram import Dispatcher, Bot, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis  # type: ignore
from src.handlers import start, solve_tasks
from settings import config

logging.basicConfig(
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s %(levelname)s %(module)s.%(funcName)s: %(message)s",
)

match config.context_storage:
    case "memory":
        fsm_storage = MemoryStorage()
    case "redis":
        fsm_storage = RedisStorage(
            Redis(host=config.redis_host, port=config.redis_port)
        )
    case _:
        fsm_storage = None

dp = Dispatcher(storage=fsm_storage)
dp.include_router(start.router)
dp.include_router(solve_tasks.router)


@dp.startup()
async def add_commands():
    await bot.set_my_commands(
        [
            types.BotCommand(command="start", description="Начать общение с ботом"),
            types.BotCommand(command="solve", description="Решать задачи"),
            types.BotCommand(command="get_result", description="Узнать количество полученных баллов и решённых задач"),
        ]
    )


bot = Bot(token=config.token.get_secret_value(), parse_mode=ParseMode.HTML)
asyncio.run(dp.start_polling(bot))
