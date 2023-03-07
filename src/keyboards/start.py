from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb = [
    [KeyboardButton(text="Начать решать")]
]

keyboard = ReplyKeyboardMarkup(keyboard=kb, one_time_keyboard=True)
