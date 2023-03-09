import typing
import pytest
from src.task_solver.models import Task


@pytest.fixture
def json_task() -> dict[str, list[dict[str, typing.Any]]]:
    """Получение 'сырых' JSON данных с задачами, подразделёнными на уровни."""
    return {
        "Простой уровень": [
            {
                "name": "Математический пример",
                "earn": 15,
                "description": "Решите пример 3 * 9",
                "result": 27
            }
        ],
        "Средний уровень": [
            {
                "name": "Уравнение",
                "earn": 25,
                "description": "Решите: 3 * x = 27. Найдите x",
                "result": 9
            },
            {
                "name": "Вторая задача в среднем уровне",
                "earn": 25,
                "description": "Решите: 5 * x = 65. Найдите x",
                "result": 13
            }
        ]
    }


@pytest.fixture
def tasks_models() -> dict[str, list[Task]]:
    """Получение моделей задач, подразделённых по уровням."""
    return {
        "Простой уровень": [
            Task(
                id=0, name="Математический пример", earn=15,
                description="Решите пример 3 * 9", result=27
            ),
        ],
        "Средний уровень": [
            Task(
                id=1, name="Уравнение", earn=25,
                description="Решите: 3 * x = 27. Найдите x", result=9
            ),
            Task(
                id=2, name="Вторая задача в среднем уровне",
                earn=25, description="Решите: 5 * x = 65. Найдите x", result=13
            ),
        ],
    }
