from uuid import uuid4
from pydantic import Field
from src.main.monitor.operator.tasksRun.model import SaveTasksRunRequestInfo as BaseSaveTasksRunRequestInfo


class SaveTasksRunRequestInfo(BaseSaveTasksRunRequestInfo):
    id: str = Field(default_factory=lambda: uuid4().__str__(), description="tasks run id", example="xxx")
    input: dict = Field(..., description="tasks run input", example={})
