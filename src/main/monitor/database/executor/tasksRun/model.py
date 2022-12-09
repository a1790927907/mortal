from uuid import uuid4
from datetime import datetime
from typing import Union, List
from typing_extensions import Literal
from pydantic import Field, BaseModel
from src.main.utils.time_utils import get_now
from src.main.monitor.frame.request.tasksRun.model import TasksRun as BaseTasksRun, \
    SearchTasksRunRequestInfo as BaseSearchTasksRunRequestInfo


class TasksRun(BaseTasksRun):
    id: str = Field(default_factory=lambda: uuid4().__str__(), description="tasks run id", example="xxx")
    updateTime: datetime = Field(default_factory=get_now, description="update time")


class PageInfo(BaseModel):
    offset: int = Field(default=0, description="偏移", example=0)
    limit: int = Field(default=100, description="上限", example=100)


class FilterInfo(BaseModel):
    by: Literal['updateTime', 'openid', 'status'] = Field(..., description="通过哪个字段过滤", example="updateTime")
    factor: Literal["eq", "lte", "gte", "lt", "gt"] = Field(..., description="比较因子", example="eq")
    value: Union[datetime, str] = Field(..., description="比较的对象", example="xxx")


class SearchTasksRunRequestInfo(BaseSearchTasksRunRequestInfo):
    pageInfo: PageInfo = Field(default=PageInfo(), description="page info")
    filterInfo: List[FilterInfo] = Field(default=None, description="filter info")
