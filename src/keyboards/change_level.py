import json
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

with open("tasks.json", "r", encoding="utf-8") as file:
    tasks = json.load(file)

kb = [[KeyboardButton(text=level_name)] for level_name in tasks]
kb.append([KeyboardButton(text="Назад")])

keyboard = ReplyKeyboardMarkup(keyboard=kb, one_time_keyboard=True)
