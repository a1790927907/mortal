from typing import Optional, List
from pydantic import Field, BaseModel
from src.main.streamStorage.frame.response.base.model import BaseResponse
from src.main.streamStorage.frame.request.connection.model import Connection as BaseConnection


class UpsertConnectionResult(BaseModel):
    id: str = Field(..., description="connection id", example="xxx")
    payload: dict = Field(..., description="connection payload", example={})


class UpsertConnectionResponse(BaseResponse):
    result: Optional[UpsertConnectionResult] = Field(default=None, description="upsert connection result")


class Connection(BaseConnection):
    id: str = Field(..., description="connection id", example="xxx")
    createTime: str = Field(..., description="create time", example="xxx")
    updateTime: str = Field(..., description="update time", example="xxx")


class GetAllConnectionsResponse(BaseResponse):
    result: Optional[List[Connection]] = Field(default=None, description="connection result")


class GetConnectionResponse(BaseResponse):
    result: Optional[Connection] = Field(default=None, description="connection result")
