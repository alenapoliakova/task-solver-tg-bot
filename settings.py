from pydantic import SecretStr, BaseSettings
from typing import Literal


class Settings(BaseSettings):
    token: SecretStr
    redis_host: str = "redis"
    redis_port: int = 6379
    context_storage: Literal['memory', 'redis'] = "memory"

    class Config:
        env_file = ".env"


config = Settings()
