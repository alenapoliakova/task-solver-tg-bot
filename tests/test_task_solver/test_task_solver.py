import pytest
from typing import Any
from unittest.mock import patch, MagicMock

from src.task_solver.task_solver import TaskSolver, Task


def test_load_tasks_from_file(json_task: dict[str, list[dict[str, Any]]], tasks_models: dict[str, list[Task]]) -> None:
    task_solver = TaskSolver()

    with patch("builtins.open", MagicMock()):
        with patch("json.load", MagicMock(side_effect=[json_task])):
            task_solver.load_tasks_from_file()

    parsed_tasks = task_solver.tasks

    assert isinstance(parsed_tasks, dict)
    assert len(parsed_tasks) == 2
    assert parsed_tasks == tasks_models
