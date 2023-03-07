from aiogram import Router, types
from aiogram.filters import CommandStart
from src.keyboards import start

router = Router()
start_msg = "Привет! Это математический бот для решения задач и получения баллов. Отправьте `Начать решать`, " \
            "чтобы приступить к решению!"


@router.message(CommandStart())
async def answer_to_start(msg: types.Message):
    await msg.answer(start_msg, reply_markup=start.keyboard)
