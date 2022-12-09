from fastapi import Query
from pydantic import Field, BaseModel
from typing import Dict, List, Optional
from src.main.streamStorage.frame.request.connection.model import Connection as BaseConnection, ConnectionPayload


class CreateConnectionRequestInfo(BaseConnection):
    ...


class UpdateConnectionRequestInfo(BaseConnection):
    payload: Optional[Dict[str, List[ConnectionPayload]]] = Field(default=None, description="connection payload")


class GetAllConnectionsRequestInfo(BaseModel):
    limit: int = Query(default=0, description="每页限制", example=0)
    offset: int = Query(default=0, description="页数偏移量", example=0)
