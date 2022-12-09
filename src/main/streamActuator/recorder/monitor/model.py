from uuid import uuid4
from typing import Optional, List
from pydantic import BaseModel, Field
from typing_extensions import Literal


class TasksRunRequestInfo(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().__str__(), description="tasks run id", example="xxx")
    input: dict = Field(..., description="tasks run input", example={})
    executeTime: float = Field(default=None, description="task run cost time", example=0.)
    status: str = Field(..., description="tasks run status summary", example="xxx")
    connectionId: str = Field(..., description="tasks run binding connection id", example="xxx")
    openid: str = Field(
        default_factory=lambda: uuid4().__str__(), description="task run id, 可重复的run id 默认uuid", example="xxx"
    )


class TaskStatusRequestInfo(BaseModel):
    status: str = Field(..., description="task status", example="xxx")
    runId: str = Field(..., description="tasks run id", example="xxx")
    taskId: str = Field(..., description="binding tasks id", example="xxx")
    executeTime: float = Field(default=None, description="task running time", example=0.)
    errorMessage: str = Field(default=None, description="task running error message if exists", example="xxx")
    output: Optional[dict] = Field(default=None, description="task out put", example={})


class TaskStatus(BaseModel):
    id: str = Field(..., description="task id", example="xxx")
    name: str = Field(..., description="task name", example="xxx")
    status: Literal['success', 'failedAndContinue', 'pending', 'skip', 'failedNotContinue'] = Field(
        ..., description="task status"
    )
    errorMessage: Optional[str] = Field(default=None, description="error message if exists", example="xxx")


class TasksRunningStatusPayload(BaseModel):
    taskStatus: List[TaskStatus] = Field(default=None, description="task status", example=None)


class TasksRunningRequestInfo(BaseModel):
    id: str = Field(default_factory=lambda: uuid4().__str__(), description="tasks running id", example="xxx")
    connectionId: str = Field(..., description="connection id", example="xxx")
    statusPayload: TasksRunningStatusPayload = Field(
        default=TasksRunningStatusPayload(), description="tasks running payload"
    )
    contextPayload: dict = Field(default={}, description="context payload", example={})
