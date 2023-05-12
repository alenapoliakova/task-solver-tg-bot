from unittest.mock import AsyncMock, MagicMock
import pytest

from src.task_solver.models import User


@pytest.mark.asyncio
async def test_get_earned_points_unknown_user_data(assert_called_once) -> None:
    """Тестирование обработчика команды /get_result. Отсутствует информация о пользователе."""
    from src.handlers.solve_tasks import get_earned_points

    message_mock = AsyncMock(answer=AsyncMock(), from_user=None)

    await get_earned_points(msg=message_mock)
    assert_called_once(message_mock.answer, "Мы не смогли идентифицировать вас")


@pytest.mark.asyncio
async def test_get_earned_points_known_user(assert_called_once) -> None:
    """Тестирование обработчика команды /get_result. Пользователь активно решал задачи."""
    from src.handlers.solve_tasks import get_earned_points, task_manager

    message_mock = AsyncMock(answer=AsyncMock(), from_user=AsyncMock(id=1))
    task_manager.solved_tasks = {1: User(user_id=1, earned_points=12, solved_ids=[1, 2, 3])}

    await get_earned_points(msg=message_mock)

    assert_called_once(message_mock.answer, "Количество решённых задач: 3\nКоличество баллов: 12")


@pytest.mark.asyncio
async def test_get_earned_points_unknown_user(assert_called_once) -> None:
    """Тестирование обработчика команды /get_result. Пользователь не решал задачи."""
    from src.handlers.solve_tasks import get_earned_points, task_manager, UserNotFound

    message_mock = AsyncMock(answer=AsyncMock(), from_user=AsyncMock(id=1))
    task_manager.get_user_by_id = MagicMock(side_effect=UserNotFound())  # type: ignore

    await get_earned_points(msg=message_mock)

    assert_called_once(message_mock.answer, "Вы пока что не решили ни одной задачи")
