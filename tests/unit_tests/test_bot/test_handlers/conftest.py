import json
import os

import pytest


@pytest.fixture
def assert_called_once():
    """Проверка, что функция была вызвана 1 раз с заданными аргументами и параметрами."""

    def _assert_called_once(mock, *args, **kwargs):
        mock.assert_called_once()
        assert mock.call_args[0] == args
        assert mock.call_args[1] == kwargs

    return _assert_called_once


@pytest.fixture(scope="module", autouse=True)
def create_tasks():
    """Создание пустого файла с задачами. После завершения тестов файл удаляется."""
    with open("tasks.json", "w+", encoding="utf-8") as file:
        json.dump({}, file)
    yield
    os.remove("tasks.json")
