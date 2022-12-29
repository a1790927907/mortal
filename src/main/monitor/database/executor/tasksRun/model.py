from uuid import uuid4
from datetime import datetime
from typing import Union, List
from src.main.utils.time_utils import get_now
from pydantic import Field, BaseModel, root_validator
from src.main.utils.time_utils import parse_date_2_datetime_object
from src.main.monitor.frame.request.tasksRun.model import TasksRun as BaseTasksRun, \
    SearchTasksRunRequestInfo as BaseSearchTasksRunRequestInfo, FilterInfo as BaseFilterInfo


class TasksRun(BaseTasksRun):
    id: str = Field(default_factory=lambda: uuid4().__str__(), description="tasks run id", example="xxx")
    updateTime: datetime = Field(default_factory=get_now, description="update time")

    @root_validator
    def convert_start_and_end_time(cls, values: dict):
        if "startTime" not in values or "endTime" not in values:
            return values
        values["startTime"] = parse_date_2_datetime_object(values["startTime"])
        values["endTime"] = parse_date_2_datetime_object(values["endTime"])
        return values


class PageInfo(BaseModel):
    offset: int = Field(default=0, description="偏移", example=0)
    limit: int = Field(default=100, description="上限", example=100)


class FilterInfo(BaseFilterInfo):
    value: Union[datetime, str] = Field(..., description="比较的对象", example="xxx")


class SearchTasksRunRequestInfo(BaseSearchTasksRunRequestInfo):
    pageInfo: PageInfo = Field(default=PageInfo(), description="page info")
    filterInfo: List[FilterInfo] = Field(default=None, description="filter info")
