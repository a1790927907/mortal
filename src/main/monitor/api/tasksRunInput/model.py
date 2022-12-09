from typing import Optional
from pydantic import Field, BaseModel
from src.main.monitor.frame.response.model import BaseResponse
from src.main.monitor.frame.request.tasksRunInput.model import TasksRunInput


class TasksRunInputEntity(TasksRunInput):
    id: str = Field(..., description="tasks run input id", example="xxx")
    createTime: str = Field(..., description="create time", example="xxx")
    updateTime: str = Field(..., description="update time", example="xxx")


class TasksRunInputResponse(BaseResponse):
    result: Optional[TasksRunInputEntity] = Field(default=None, description="tasks run input result")


class SaveTasksRunInputResult(BaseModel):
    id: str = Field(..., description="tasks run input id", example="xxx")
    runId: str = Field(..., description="tasks run input binding tasks run id", example="xxx")


class SaveTasksRunInputResponse(BaseResponse):
    result: Optional[SaveTasksRunInputResult] = Field(default=None, description="save tasks run input result")
