from typing import Any
from pydantic import BaseModel, Field


class Output(BaseModel):
    data: Any = Field(..., description="output value")
    extra: dict = Field(..., description="extra value", example={})


class TaskOutput(BaseModel):
    taskStatusId: str = Field(..., description="binding task status id", example="xxx")
    taskId: str = Field(..., description="binding task id", example="xxx")
    output: Output = Field(default=None, description="task output", example="xxx")
