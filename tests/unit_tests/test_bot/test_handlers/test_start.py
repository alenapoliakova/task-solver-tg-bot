from unittest.mock import AsyncMock

import pytest

from src.handlers.start import answer_to_start, START_MSG, start


@pytest.mark.asyncio
async def test_start(assert_called_once):
    """Тестирование обработчика команды /start."""
    message_mock = AsyncMock(answer=AsyncMock())
    await answer_to_start(msg=message_mock)
    assert_called_once(message_mock.answer, START_MSG, reply_markup=start.keyboard)
