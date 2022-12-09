from pydantic import BaseModel, Field


class TaskStatus(BaseModel):
    status: str = Field(..., description="task status", example="xxx")
    runId: str = Field(..., description="tasks run id", example="xxx")
    taskId: str = Field(..., description="binding tasks id", example="xxx")
    executeTime: float = Field(default=None, description="task running time", example=0.)
    errorMessage: str = Field(default=None, description="task running error message if exists", example="xxx")
