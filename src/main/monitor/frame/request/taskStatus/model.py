from typing import Optional
from pydantic import BaseModel, Field


class TaskStatus(BaseModel):
    status: str = Field(..., description="task status", example="xxx")
    runId: str = Field(..., description="tasks run id", example="xxx")
    taskId: str = Field(..., description="binding tasks id", example="xxx")
    executeTime: float = Field(default=None, description="task running time", example=0.)
    errorMessage: str = Field(default=None, description="task running error message if exists", example="xxx")
    retryTime: int = Field(default=0, description="任务重试次数", example=0)
    startTime: Optional[str] = Field(default=None, description="开始时间", example="2022-12-14 00:00:00")
    endTime: Optional[str] = Field(default=None, description="开始时间", example="2022-12-14 00:00:00")
