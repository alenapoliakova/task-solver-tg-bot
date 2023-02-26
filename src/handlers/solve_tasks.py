from aiogram import Router, types
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from src.keyboards import change_level
from src.task_manager import TaskManager

router = Router()

task_manager = TaskManager()
task_manager.load_tasks_from_file()


class TaskForm(StatesGroup):
    level = State()  # example: easy / middle / hard
    task_id = State()  # integer type
    result = State()  # example: ok / not ok

    # solved_tasks = State()
    # date = State()


@router.message(Text("Начать решать"))
async def change_task_level(msg: types.Message, state: FSMContext):
    """Отправить уровни, в которых есть задачи."""
    await msg.answer("Выберите уровень", reply_markup=change_level.keyboard)
    await state.set_state(TaskForm.level)


@router.message(TaskForm.level)
async def send_task(msg: types.Message, state: FSMContext):
    """Отправить задачу, которая соответствует выбранному уровню."""
    if (level := msg.text) == "Назад":
        await state.clear()
        return
    if level not in task_manager.get_levels():
        return await msg.reply(f"Вы ввели неизвестный уровень. Выберите уровень:", reply_markup=change_level.keyboard)
    task = task_manager.generate_random_task_by_level(level)
    await state.update_data(task_id=task.id)

    data = f'Задача "{task.name}"\nУровень: {level}\n\n{task.description}'
    await msg.reply(data)
    await state.set_state(TaskForm.task_id)

# TODO: add handler for matching result
