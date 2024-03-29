import logging
from aiogram import Router, types
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from src.keyboards import change_level
from src.task_solver.errors import UserNotFound, TaskAlreadySolved
from src.task_solver.task_solver import TaskSolver

router = Router()

task_manager = TaskSolver()
task_manager.load_tasks_from_file()


class TaskForm(StatesGroup):
    """FSM (finish state machine) для хранения прогресса пользователя в решении задач."""
    level = State()  # example: easy / middle / hard
    task_id = State()  # integer type


@router.message(Command("get_result"))
async def get_earned_points(msg: types.Message):
    """Получить заработанные баллы и количество решённых задач."""
    if not msg.from_user:
        return await msg.answer("Мы не смогли идентифицировать вас")

    try:
        user = task_manager.get_user_by_id(msg.from_user.id)
    except UserNotFound:
        return await msg.answer("Вы пока что не решили ни одной задачи")
    await msg.answer(f"Количество решённых задач: {len(user.solved_ids)}\n"
                     f"Количество баллов: {user.earned_points}")
    logging.info(f"get_result: {msg.from_user}={len(user.solved_ids)}, {user.earned_points}")


@router.message(Text("Начать решать"))
@router.message(Command("solve"))
async def change_task_level(msg: types.Message, state: FSMContext):
    """Отправить уровни, в которых есть задачи."""
    await msg.answer("Выберите уровень", reply_markup=change_level.keyboard)
    await state.set_state(TaskForm.level)
    logging.info(f"start solve: {msg.from_user}")


@router.message(TaskForm.level)
async def send_task(msg: types.Message, state: FSMContext):
    """Отправить задачу, которая соответствует выбранному уровню."""
    if (level := msg.text) in ("Назад", "/start", "/cancel"):
        return await state.clear()
    if level not in task_manager.get_levels():
        return await msg.reply(
            "Вы ввели неизвестный уровень. Выберите уровень:",
            reply_markup=change_level.keyboard
        )
    task = task_manager.generate_random_task_by_level(level)
    await state.update_data(task_id=task.id)

    data = f'Задача "{task.name}"\nУровень: {level}\n\n{task.description}'
    await msg.reply(data)
    await state.set_state(TaskForm.task_id)
    logging.info(f"send task: {msg.from_user}, task={task}")


@router.message(TaskForm.task_id)
async def verify_result(msg: types.Message, state: FSMContext):
    """Проверить ответ пользователя на выбранную задачу."""
    task = task_manager.get_task_by_id(task_id=(await state.get_data())["task_id"])
    if msg.text != str(task.result):
        if msg.from_user:
            name = f"{msg.from_user.first_name} {msg.from_user.last_name}"
            logging.info(f"not solved: {name} {msg.from_user.username} {task}")
        return await msg.answer("Вы ответили неправильно, повторите попытку")
    await state.clear()

    try:
        if msg.from_user:
            user = task_manager.save_user_solved_task(
                task=task,
                user_id=msg.from_user.id,
                name=f"{msg.from_user.first_name} {msg.from_user.last_name}",
                user_name=msg.from_user.username
            )
            logging.info(f"solved: user={user} {task}")
            return await msg.answer(f"Вы ответили правильно и получили "
                                    f"{task.earn} балл(-а)!")
    except TaskAlreadySolved:
        return await msg.answer("Баллы за задачу уже были начислены")
    logging.info(f"solved but unknown: {task}, {msg}")
    return await msg.answer("Нам не удалось записать ваш ответ")
