from typing import Dict, List
from pydantic import BaseModel, Field


class ConnectionPayload(BaseModel):
    id: str = Field(..., description="task id", example="xxx")
    name: str = Field(..., description="task name", example="xxx")


class SaveConnectionRequestInfo(BaseModel):
    name: str = Field(..., description="connection name", example="xxx")
    payload: Dict[str, List[ConnectionPayload]] = Field(..., description="connection payload")
    referenceId: int = Field(..., description="n8n中workflow的id", example=1)


class TaskPayload(BaseModel):
    parameters: dict = Field(..., description="task参数", example={})


class SaveTaskRequestInfo(BaseModel):
    taskId: str = Field(..., description="task id", example="xxx")
    name: str = Field(..., description="task name", example="xxx")
    type: str = Field(..., description="task type", example="xxx")
    payload: TaskPayload = Field(..., description="task payload")
    connectionId: str = Field(..., description="对应connection的id", example="xxx")


class SaveSchemaRequestInfo(BaseModel):
    info: dict = Field(..., description="json schema", example={})
    connectionId: str = Field(..., description="connection id")
