from typing import Optional, List
from pydantic import BaseModel, Field
from src.main.monitor.frame.response.model import BaseResponse
from src.main.monitor.frame.request.tasksRunning.model import TasksRunning


class OperateTasksRunningResult(BaseModel):
    id: str = Field(..., description="tasks running id", example="xxx")


class DeleteTasksRunningResult(OperateTasksRunningResult):
    ...


class SaveTasksRunningResult(OperateTasksRunningResult):
    connectionId: str = Field(..., description="connection id", example="xxx")


class SaveTasksRunningResponse(BaseResponse):
    result: Optional[SaveTasksRunningResult] = Field(default=None, description="save tasks running result")


class DeleteTasksRunningResponse(BaseResponse):
    result: Optional[DeleteTasksRunningResult] = Field(default=None, description="delete tasks running result")


class TasksRunningEntity(TasksRunning):
    id: str = Field(..., description="tasks run input id", example="xxx")
    createTime: str = Field(..., description="create time", example="xxx")
    updateTime: str = Field(..., description="update time", example="xxx")


class TasksRunningResponse(BaseResponse):
    result: Optional[TasksRunningEntity] = Field(default=None, description="tasks running result")


class MultipleTasksRunningResponse(BaseResponse):
    result: Optional[List[TasksRunningEntity]] = Field(default=None, description="tasks running result")
