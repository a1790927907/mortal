from typing import List, Optional
from typing_extensions import Literal
from pydantic import BaseModel, Field


class TaskStatus(BaseModel):
    id: str = Field(..., description="task id", example="xxx")
    name: str = Field(..., description="task name", example="xxx")
    status: Literal['success', 'failedAndContinue', 'pending', 'skip', 'failedNotContinue'] = Field(
        ..., description="task status"
    )
    errorMessage: Optional[str] = Field(default=None, description="error message if exists", example="xxx")


class TasksRunningStatusPayload(BaseModel):
    taskStatus: List[TaskStatus] = Field(default=None, description="task status", example=None)


class TasksRunning(BaseModel):
    connectionId: str = Field(..., description="connection id", example="xxx")
    statusPayload: TasksRunningStatusPayload = Field(
        default=TasksRunningStatusPayload(), description="tasks running payload"
    )
    contextPayload: dict = Field(default={}, description="context payload", example={})
