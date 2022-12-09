from typing import List, Optional
from pydantic import BaseModel, Field


class RequestInfo(BaseModel):
    input: dict = Field(..., description="入参", example={})
    connection: dict = Field(..., description="connection", example={})
    tasks: List[dict] = Field(..., description="tasks", example=[])
    record: Optional[dict] = Field(default={}, description="日志记录相关")
    taskStatus: Optional[List[dict]] = Field(default=None, description="task status record", example=None)
    context: Optional[dict] = Field(default=None, description="context", example=None)
