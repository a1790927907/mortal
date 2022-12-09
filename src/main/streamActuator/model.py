from typing import Dict, List
from pydantic import BaseModel, Field


class ConnectionPayload(BaseModel):
    id: str = Field(..., description="task id", example="xxx")
    name: str = Field(..., description="task name", example="xxx")


class Connection(BaseModel):
    id: str = Field(..., description="connection id", example="xxx")
    payload: Dict[str, List[ConnectionPayload]] = Field(..., description="connection payload")


class TaskPayload(BaseModel):
    parameters: dict = Field(..., description="task参数", example={})


class Task(BaseModel):
    id: str = Field(..., description="task id", example="xxx")
    name: str = Field(..., description="task name", example="xxx")
    type: str = Field(..., description="task type", example="xxx")
    payload: TaskPayload = Field(..., description="task payload")
