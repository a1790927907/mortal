from uuid import uuid4
from typing import List, Optional
from typing_extensions import Literal
from pydantic import BaseModel, Field


class TasksRun(BaseModel):
    executeTime: float = Field(default=None, description="task run cost time", example=0.)
    status: str = Field(..., description="tasks run status summary", example="xxx")
    connectionId: str = Field(..., description="tasks run binding connection id", example="xxx")
    startTime: str = Field(..., description="开始时间", example="2022-12-14 00:00:00")
    endTime: str = Field(..., description="开始时间", example="2022-12-14 00:00:00")
    openid: str = Field(
        default_factory=lambda: uuid4().__str__(), description="task run id, 可重复的run id 默认uuid", example="xxx"
    )


class PageInfo(BaseModel):
    page: int = Field(default=1, description="页数", example=1)
    size: int = Field(default=100, description="当前页大小", example=100)


class Order(BaseModel):
    by: Literal['updateTime', 'startTime', 'endTime'] = Field(
        default="startTime", description="通过哪个字段排序", example="updateTime"
    )
    type: Literal["asc", "desc"] = Field(default="desc", description="升序还是降序", example="desc")


class FilterInfo(BaseModel):
    by: Literal['updateTime', 'openid', 'status', 'endTime', 'startTime'] = Field(
        ..., description="通过哪个字段过滤", example="updateTime"
    )
    factor: Literal["eq", "lte", "gte", "lt", "gt"] = Field(..., description="比较因子", example="eq")
    value: str = Field(..., description="比较的对象(目前只支持字符串)", example="xxx")


class SearchTasksRunRequestInfo(BaseModel):
    pageInfo: PageInfo = Field(default=PageInfo(), description="page info")
    order: Order = Field(default=Order(), description="order info")
    filterInfo: Optional[List[FilterInfo]] = Field(default=None, description="filter info")
    connectionId: str = Field(..., description="connection id", example="xxx")
