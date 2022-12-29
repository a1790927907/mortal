from uuid import uuid4
from datetime import datetime
from pydantic import Field, root_validator
from src.main.utils.time_utils import get_now, parse_date_2_datetime_object
from src.main.monitor.frame.request.taskStatus.model import TaskStatus as BaseTaskStatus


class TaskStatus(BaseTaskStatus):
    id: str = Field(default_factory=lambda: uuid4().__str__(), description="task status id", example="xxx")
    updateTime: datetime = Field(default_factory=get_now, description="update time")

    @root_validator
    def convert_start_and_end_time(cls, values: dict):
        if "startTime" not in values or "endTime" not in values:
            return values
        values["startTime"] = parse_date_2_datetime_object(values["startTime"], raise_exception=False)
        values["endTime"] = parse_date_2_datetime_object(values["endTime"], raise_exception=False)
        return values
