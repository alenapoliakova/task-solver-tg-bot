from typing import Literal
from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    """Класс, необходимый для считывания значений переменного окружения."""
    token: SecretStr
    redis_host: str = "redis"
    redis_port: int = 6379
    context_storage: Literal['memory', 'redis'] = "memory"

    class Config:
        """Конфиг для pydantic модели."""
        env_file = ".env"


config = Settings()  # type: ignore
