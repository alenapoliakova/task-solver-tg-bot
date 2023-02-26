import json
import random
from dataclasses import dataclass
from typing import Any


@dataclass
class Task:
    id: int
    name: str
    earn: int
    description: str
    result: Any


class TaskManager:

    def __init__(self):
        self.tasks: dict[str, list[Task]] = {}

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
        # self.tasks = {level: [Task(**task) for task in tasks[level]] for level in tasks}

    def generate_random_task_by_level(self, level: str) -> Task:
        if level not in self.tasks:
            raise ValueError(f"Unknown level_name = {level}")
        return random.choice(self.tasks[level])

    def generate_random_task(self) -> Task:
        level = random.choice(list(self.tasks))
        return self.generate_random_task_by_level(level)

    def get_task_by_id(self, id_: int) -> Task:
        for level in self.tasks:
            for task in self.tasks[level]:
                if task.id == id_:
                    return task
        raise ValueError(f"Task with id = {id_} not found")

    def get_levels(self) -> list[str]:
        return list(self.tasks.keys())
