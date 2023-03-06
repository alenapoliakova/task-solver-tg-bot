class BaseError(Exception):
    ...


class TaskNotFound(BaseError):
    ...


class LevelNotFound(BaseError):
    ...


class UserNotFound(BaseError):
    ...


class TaskAlreadySolved(BaseError):
    ...
