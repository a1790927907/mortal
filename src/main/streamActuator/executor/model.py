from typing import Any
from pydantic import BaseModel, Field


class ExecutorResult(BaseModel):
    value: Any = Field(..., description="result", example="")
    extraValue: dict = Field(default={}, description="extra something", example={})
    executeTime: float = Field(default=None, description="执行时长", example=0.)
