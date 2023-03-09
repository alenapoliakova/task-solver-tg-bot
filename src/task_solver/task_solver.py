import json
import random

from .models import Task, User
from .errors import TaskNotFound, LevelNotFound, UserNotFound, TaskAlreadySolved


class TaskSolver:
    """Класс для хранения задач по уровням и кэширования решённых задач у пользователя."""

    def __init__(self):
        self.tasks: dict[str, list[Task]] = {}
        self.solved_tasks: dict[int, User] = {}

    def load_tasks_from_file(self, file_name="tasks.json") -> None:
        """
        Загрузка задач из JSON файла.
        Parameters:
            file_name: Путь до JSON файла. По умолчанию: 'tasks.json'.
        """
        with open(file_name, "r", encoding="utf-8") as file:
            tasks = json.load(file)
        self.tasks = {}
        idx = 0
        for level in tasks:
            prepared_tasks = []
            for task in tasks[level]:
                prepared_tasks.append(Task(**task, id=idx))
                idx += 1
            self.tasks[level] = prepared_tasks

    def generate_random_task_by_level(self, level: str) -> Task:
        """
        Генерация случайной задачи в заданном уровне.
        Parameters:
            level: Уровень, в которой находятся задачи.
        Notes:
            - При вызове метода с неизвестным методом вызовется ошибка LevelNotFound.
        """
        if level not in self.tasks:
            raise LevelNotFound
        return random.choice(self.tasks[level])

    def generate_random_task(self) -> Task:
        """Генерация случайной задачи в случайном уровне."""
        level = random.choice(list(self.tasks))
        return self.generate_random_task_by_level(level)

    def get_task_by_id(self, id: int) -> Task:
        """
        Получение задачи по её уникальному идентификатору, заданному при считывании файла.
        Parameters:
            id: ID задачи.
        Returns: Задача с переданным ID.
        Notes:
            - При отсутствии задачи с заданным ID вызовется ошибка TaskNotFound.
        """
        for tasks in self.tasks.values():
            for task in tasks:
                if task.id == id:
                    return task
        raise TaskNotFound(f"Task with id = {id} not found")

    def get_levels(self) -> list[str]:
        """Получение названий всех доступных уровней, в которых есть задачи для решения."""
        return list(self.tasks.keys())

    def save_user_solved_task(self, task: Task, user_id: int,
                              name: str | None = None,
                              user_name: str | None = None) -> User:
        """
        Кеширование решения задачи, которую решил пользователь.
        Parameters:
            task: Задача.
            user_id: ID пользователя.
            name: Имя пользователя (optional).
            user_name: Логин пользователя (optional).
        Returns:
            user: Пользователь со всей историей решения задач.
        """
        if not (user := self.solved_tasks.get(user_id)):
            user = User(
                user_id=user_id,
                name=name,
                user_name=user_name,
            )
            self.solved_tasks[user_id] = user
        if task.id in user.solved_ids:
            raise TaskAlreadySolved()
        user.solved_ids.append(task.id)
        user.earned_points += task.earn
        return user

    def get_user_by_id(self, user_id: int) -> User:
        """
        Получение пользователя по его уникальному идентификатору.
        Parameters:
            user_id: ID пользователя.
        Returns:
            user: Пользователь со всей историей решения задач.
        Notes:
             - Если пользователь не был найден, вызовется ошибка UserNotFound.
        """
        if not (user := self.solved_tasks.get(user_id)):
            raise UserNotFound
        return user
