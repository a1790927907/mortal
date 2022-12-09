from typing import List
from pydantic import BaseModel, Field


class RequestInfo(BaseModel):
    nodes: List[dict] = Field(..., description="node info", example=[])
    connections: dict = Field(..., description="connection info", example={})
