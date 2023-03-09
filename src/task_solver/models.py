from dataclasses import dataclass, field
from typing import Any


@dataclass
class Task:
    id: int
    name: str
    earn: int
    description: str
    result: Any


@dataclass
class User:
    user_id: int
    name: str | None = None
    user_name: str | None = None
    solved_ids: list[int] = field(default_factory=list)
    earned_points: int = 0
