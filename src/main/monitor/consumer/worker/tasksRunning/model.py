from uuid import uuid4
from pydantic import Field, BaseModel
from typing_extensions import Literal
from src.main.monitor.operator.tasksRunning.model import SaveTasksRunningRequestInfo as BaseSaveTasksRunningRequestInfo


class SaveTasksRunningRequestInfo(BaseSaveTasksRunningRequestInfo):
    id: str = Field(default_factory=lambda: uuid4().__str__(), description="tasks running id", example="xxx")


class DeleteTasksRunningRequestInfo(BaseModel):
    id: str = Field(..., description="tasks running id", example="xxx")
    type: Literal['delete'] = Field(..., description="request type", example="delete")
