import json
import random

from .models import Task, User
from src.task_solver.errors import (TaskNotFound, LevelNotFound, UserNotFound,
                                    TaskAlreadySolved)


class TaskSolver:

    def __init__(self):
        self.tasks: dict[str, list[Task]] = {}
        self.solved_tasks: dict[int, User] = {}

    def load_tasks_from_file(self) -> None:
        with open("tasks.json", "r", encoding="utf-8") as file:
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
        if level not in self.tasks:
            raise LevelNotFound
        return random.choice(self.tasks[level])

    def generate_random_task(self) -> Task:
        level = random.choice(list(self.tasks))
        return self.generate_random_task_by_level(level)

    def get_task_by_id(self, id: int) -> Task:
        for level in self.tasks:
            for task in self.tasks[level]:
                if task.id == id:
                    return task
        raise TaskNotFound(f"Task with id = {id} not found")

    def get_levels(self) -> list[str]:
        return list(self.tasks.keys())

    def save_user_solved_task(self, task: Task, user_id: int,
                              name: str | None = None,
                              user_name: str | None = None) -> User:
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
        if not (user := self.solved_tasks.get(user_id)):
            raise UserNotFound
        return user
