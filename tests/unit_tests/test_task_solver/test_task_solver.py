from typing import Any
from unittest.mock import patch, MagicMock

import pytest

from src.task_solver.task_solver import (TaskSolver, Task, User, TaskAlreadySolved, UserNotFound,
                                         LevelNotFound, TaskNotFound)


def test_load_tasks_from_file(
        json_task: dict[str, list[dict[str, Any]]],
        tasks_models: dict[str, list[Task]]) -> None:
    """Загрузка задач в TaskSolver."""
    task_solver = TaskSolver()

    with patch("builtins.open", MagicMock()):
        with patch("json.load", MagicMock(side_effect=[json_task])):
            task_solver.load_tasks_from_file()

    parsed_tasks = task_solver.tasks

    assert isinstance(parsed_tasks, dict)
    assert len(parsed_tasks) == 2
    assert parsed_tasks == tasks_models


def test_save_user_solved_task() -> None:
    """Сохранение решённой задачи."""
    task_solver = TaskSolver()

    user_id, task = 1, Task(id=1, name="Задача", earn=5,
                            description="Решите пример: 11 * 14", result=154)

    task_solver.save_user_solved_task(
        task=task, user_id=user_id
    )

    assert task_solver.solved_tasks == {user_id: User(user_id=user_id, solved_ids=[task.id],
                                                      earned_points=task.earn)}


def test_save_user_solved_task_already_solved() -> None:
    """Сохранение решённой задачи, если она уже решена."""
    task_solver = TaskSolver()

    user_id, task = 1, Task(id=1, name="Задача", earn=5,
                            description="Решите пример: 11 * 14", result=154)

    # первое сохранение задачи
    task_solver.save_user_solved_task(
        task=task, user_id=user_id
    )

    # второе сохранение задачи - ошибка
    with pytest.raises(TaskAlreadySolved):
        task_solver.save_user_solved_task(
            task=task, user_id=user_id
        )


def test_get_user_solved_tasks() -> None:
    """Получение решённых задач пользователя."""
    task_solver = TaskSolver()

    user_id, task = 1, Task(id=1, name="Задача", earn=5,
                            description="Решите пример: 11 * 14", result=154)

    task_solver.save_user_solved_task(
        task=task, user_id=user_id
    )

    assert task_solver.get_user_by_id(user_id) == User(user_id=user_id, solved_ids=[task.id],
                                                       earned_points=task.earn)


def test_get_user_solved_tasks_not_found() -> None:
    """Получение решённых задач пользователя, если пользователь не найден."""
    task_solver = TaskSolver()

    user_id, task = 1, Task(id=1, name="Задача", earn=5,
                            description="Решите пример: 11 * 14", result=154)

    task_solver.save_user_solved_task(
        task=task, user_id=user_id
    )

    with pytest.raises(UserNotFound):
        task_solver.get_user_by_id(user_id + 1)


def test_generate_random_task_by_level() -> None:
    """Получение случайной задачи по уровню сложности."""
    task_solver = TaskSolver()

    # добавление задач в TaskSolver
    task_solver.tasks = {
        "easy": [
            Task(id=1, name="Задача 1", earn=5, description="Решите пример: 11 * 14", result=154),
            Task(id=2, name="Задача 2", earn=3, description="Решите пример: 11 * 14", result=154),
        ],
        "middle": [
            Task(id=3, name="Задача 3", earn=15, description="Решите пример: 11 * 14", result=154),
        ],
    }

    with patch("random.choice", MagicMock(side_effect=lambda x: task_solver.tasks["easy"][0])):
        task = task_solver.generate_random_task_by_level(level="easy")

    assert task == task_solver.tasks["easy"][0]


def test_generate_random_task_by_level_not_found() -> None:
    """Получение случайной задачи по уровню сложности, если задачи не найдены."""
    task_solver = TaskSolver()

    # добавление задач в TaskSolver
    task_solver.tasks = {
        "easy": [],
        "middle": [
            Task(id=3, name="Задача 3", earn=15, description="Решите пример: 11 * 14", result=154),
        ],
    }

    with pytest.raises(LevelNotFound):
        task_solver.generate_random_task_by_level(level="easy")


def test_generate_random_task() -> None:
    """Получение случайной задачи."""
    task_solver = TaskSolver()

    # добавление задач в TaskSolver
    task_solver.tasks = {
        "easy": [
            Task(id=1, name="Задача 11", earn=5, description="Решите пример: 11 * 14", result=154),
            Task(id=2, name="Задача 2", earn=3, description="Решите пример: 11 * 14", result=154),
        ],
        "middle": [
            Task(id=3, name="Задача 3", earn=15, description="Решите пример: 11 * 14", result=154),
        ],
    }

    with patch("random.choice", MagicMock(side_effect=["easy", task_solver.tasks["easy"][1]])):
        task = task_solver.generate_random_task()

    assert task == task_solver.tasks["easy"][1]


def test_generate_random_task_not_found() -> None:
    """Получение случайной задачи, если задачи не найдены."""
    task_solver = TaskSolver()

    # добавление задач в TaskSolver
    task_solver.tasks = {
        "easy": [],
        "middle": [],
    }

    with pytest.raises(LevelNotFound):
        task_solver.generate_random_task()


def test_get_task_by_id() -> None:
    """Получение задачи по id."""
    task_solver = TaskSolver()

    # добавление задач в TaskSolver
    task_solver.tasks = {
        "easy": [
            Task(id=1, name="Задача 11", earn=5, description="Решите пример: 11 * 14", result=154),
        ],
    }

    task = task_solver.get_task_by_id(task_id=1)

    assert task.id == 1
    assert task == task_solver.tasks["easy"][0]


def test_get_task_by_id_not_found() -> None:
    """Получение задачи по id, если задача не найдена."""
    task_solver = TaskSolver()

    with pytest.raises(TaskNotFound):
        task_solver.get_task_by_id(task_id=1)


def test_get_levels() -> None:
    """Получение всех уровней сложности."""
    task_solver = TaskSolver()

    task_solver.tasks = {
        "easy": [],
    }

    assert task_solver.get_levels() == ["easy"]
