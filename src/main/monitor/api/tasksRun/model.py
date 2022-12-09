from typing import Optional, List
from pydantic import BaseModel, Field
from src.main.monitor.frame.response.model import BaseResponse
from src.main.monitor.frame.request.tasksRun.model import TasksRun


class TasksRunEntity(TasksRun):
    id: str = Field(..., description="tasks run id", example="xxx")
    createTime: str = Field(..., description="create time", example="xxx")
    updateTime: str = Field(..., description="update time", example="xxx")


class SaveTasksRunResult(BaseModel):
    id: str = Field(..., description="tasks run id", example="xxx")
    connectionId: str = Field(..., description="connection id", example="xxx")
    openid: str = Field(..., description="open id", example="xxx")


class SaveTasksRunResponse(BaseResponse):
    result: Optional[SaveTasksRunResult] = Field(default=None, description="save tasks run result")


class TasksRunResponse(BaseResponse):
    result: Optional[TasksRunEntity] = Field(default=None, description="tasks run entity response")


class MultipleTasksRunResponse(BaseResponse):
    result: Optional[List[TasksRunEntity]] = Field(default=None, description="tasks run entity response")


class SearchTasksRunsResult(BaseModel):
    tasksRuns: List[TasksRunEntity] = Field(..., description="tasks run entity response")
    total: Optional[int] = Field(default=None, description="total count", example=1000)


class SearchTasksRunsResponse(BaseResponse):
    result: Optional[SearchTasksRunsResult] = Field(default=None, description="search tasks runs entity response")
