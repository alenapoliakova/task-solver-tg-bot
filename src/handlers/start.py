from aiogram import Router, types
from aiogram.filters import CommandStart
from src.keyboards import start

router = Router()
START_MSG = "Привет! Это математический бот для решения задач и получения баллов. " \
            "Отправьте `Начать решать`, чтобы приступить к решению!"


@router.message(CommandStart())
async def answer_to_start(msg: types.Message):
    """Ответить пользователю приветственное сообщение после отправки '/start'."""
    await msg.answer(START_MSG, reply_markup=start.keyboard)
