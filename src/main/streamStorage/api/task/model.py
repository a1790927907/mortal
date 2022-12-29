from typing import Optional, List
from pydantic import BaseModel, Field
from src.main.streamStorage.frame.response.base.model import BaseResponse
from src.main.streamStorage.frame.request.task.model import Task as BaseTask


class UpsertTaskResult(BaseModel):
    id: str = Field(..., description="task id", example="xxx")
    name: str = Field(..., description="task name", example="xxx")


class UpsertTaskResponse(BaseResponse):
    result: Optional[UpsertTaskResult] = Field(default=None, description="upsert task result")


class DeleteTaskResponse(UpsertTaskResponse):
    ...


class Task(BaseTask):
    id: str = Field(..., description="connection id", example="xxx")
    createTime: str = Field(..., description="create time", example="xxx")
    updateTime: str = Field(..., description="update time", example="xxx")


class GetTasksResponse(BaseResponse):
    result: Optional[List[Task]] = Field(default=None, description="task result")


class GetTaskResponse(BaseResponse):
    result: Optional[Task] = Field(default=None, description="task result")
