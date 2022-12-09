from typing import Optional, List
from pydantic import BaseModel, Field
from src.main.monitor.frame.response.model import BaseResponse
from src.main.monitor.frame.request.taskStatus.model import TaskStatus


class TaskStatusEntity(TaskStatus):
    id: str = Field(..., description="tasks status id", example="xxx")
    createTime: str = Field(..., description="create time", example="xxx")
    updateTime: str = Field(..., description="update time", example="xxx")


class SaveTaskStatusResult(BaseModel):
    id: str = Field(..., description="tasks status id", example="xxx")
    runId: str = Field(..., description="task status binding run id", example="xxx")
    taskId: str = Field(..., description="task status binding task id", example="xxx")
    status: str = Field(..., description="task status info", example="xxx")


class SaveTaskStatusResponse(BaseResponse):
    result: Optional[SaveTaskStatusResult] = Field(default=None, description="save task status response")


class TaskStatusResponse(BaseResponse):
    result: Optional[TaskStatusEntity] = Field(default=None, description="task status entity response")


class MultipleTaskStatusResponse(BaseResponse):
    result: Optional[List[TaskStatusEntity]] = Field(default=None, description="task status entity response")

