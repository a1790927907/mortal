from typing import List, Optional
from pydantic import BaseModel, Field
from src.main.streamController.frame.response.model import BaseResponse


class TaskStatus(BaseModel):
    id: str = Field(..., description="tasks status id", example="xxx")
    status: str = Field(..., description="task status", example="xxx")
    runId: str = Field(..., description="tasks run id", example="xxx")
    taskId: str = Field(..., description="binding tasks id", example="xxx")
    executeTime: float = Field(default=None, description="task running time", example=0.)
    errorMessage: str = Field(default=None, description="task running error message if exists", example="xxx")
    createTime: str = Field(..., description="create time", example="xxx")
    updateTime: str = Field(..., description="update time", example="xxx")


class TaskPayload(BaseModel):
    parameters: dict = Field(..., description="task参数", example={})


class Task(BaseModel):
    id: str = Field(..., description="connection id", example="xxx")
    name: str = Field(..., description="task name", example="xxx")
    type: str = Field(..., description="task type", example="xxx")
    payload: TaskPayload = Field(..., description="task payload")
    connectionId: str = Field(..., description="对应connection的id", example="xxx")
    createTime: str = Field(..., description="create time", example="xxx")
    updateTime: str = Field(..., description="update time", example="xxx")


class TaskStatusLoadedEntity(BaseModel):
    taskStatus: TaskStatus = Field(..., description="task status entity")
    task: Task = Field(..., description="task entity")


class TaskStatusLoadedResult(BaseModel):
    inExecution: List[TaskStatusLoadedEntity] = Field(..., description="需要执行的tasks")
    outExecution: List[TaskStatusLoadedEntity] = Field(..., description="不需要执行的tasks")


class TaskStatusLoadedResponse(BaseResponse):
    result: Optional[List[TaskStatusLoadedResult]] = Field(default=None, description="task status loaded result")
