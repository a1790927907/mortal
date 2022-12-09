from uuid import uuid4
from pydantic import Field
from datetime import datetime
from src.main.utils.time_utils import get_now
from src.main.monitor.frame.request.taskOutput.model import TaskOutput as BaseTaskOutput


class TaskOutput(BaseTaskOutput):
    id: str = Field(default_factory=lambda: uuid4().__str__(), description="tasks run id", example="xxx")
    updateTime: datetime = Field(default_factory=get_now, description="update time")
