from typing import Dict, List
from pydantic import BaseModel, Field


class ConnectionPayload(BaseModel):
    id: str = Field(..., description="task id", example="xxx")
    name: str = Field(..., description="task name", example="xxx")


class Connection(BaseModel):
    name: str = Field(..., description="connection name", example="xxx")
    payload: Dict[str, List[ConnectionPayload]] = Field(..., description="connection payload")
    referenceId: int = Field(..., description="n8n中workflow的id", example=1)
