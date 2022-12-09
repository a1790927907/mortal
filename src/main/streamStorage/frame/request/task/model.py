from pydantic import BaseModel, Field


class TaskPayload(BaseModel):
    parameters: dict = Field(..., description="task参数", example={})


class Task(BaseModel):
    name: str = Field(..., description="task name", example="xxx")
    type: str = Field(..., description="task type", example="xxx")
    payload: TaskPayload = Field(..., description="task payload")
    connectionId: str = Field(..., description="对应connection的id", example="xxx")
