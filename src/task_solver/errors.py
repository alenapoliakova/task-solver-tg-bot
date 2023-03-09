class BaseError(Exception):
    """Базовый класс для всех ошибок модуля Task Solver."""


class TaskNotFound(BaseError):
    """Задача не найдена."""


class LevelNotFound(BaseError):
    """Уровень не найден"""


class UserNotFound(BaseError):
    """Пользователь не найден."""


class TaskAlreadySolved(BaseError):
    """Задача уже была решена."""
