from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from src.main.streamParser.frame.response.model import BaseResponse


class ConnectionPayload(BaseModel):
    id: str = Field(..., description="task id", example="xxx")
    name: str = Field(..., description="task name", example="xxx")


class TaskPayload(BaseModel):
    parameters: dict = Field(..., description="task参数", example={})


class Task(BaseModel):
    id: str = Field(..., description="task id", example="xxx")
    name: str = Field(..., description="task name", example="xxx")
    type: str = Field(..., description="task type", example="xxx")
    payload: TaskPayload = Field(..., description="task payload")


class ParsedFlowResult(BaseModel):
    connection: Dict[str, List[ConnectionPayload]] = Field(..., description="connection payload")
    tasks: List[Task] = Field(..., description="tasks")


class ParsedFlowResponse(BaseResponse):
    result: Optional[ParsedFlowResult] = Field(default=None, description="parsed result")
