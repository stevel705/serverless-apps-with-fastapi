from dataclasses import dataclass
from enum import Enum
from uuid import UUID


class TaskStatus(Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    CLOSED = "CLOSED"


@dataclass
class Task:
    id: UUID
    title: str
    status: TaskStatus
    owner: str

    @classmethod
    def create(cls, id_: UUID, title: str, owner: str) -> "Task":
        return cls(id=id_, title=title, status=TaskStatus.OPEN, owner=owner)
