from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from src.main.streamController.frame.response.model import BaseResponse


class ConnectionPayload(BaseModel):
    id: str = Field(..., description="task id", example="xxx")
    name: str = Field(..., description="task name", example="xxx")


class Connection(BaseModel):
    id: str = Field(..., description="connection id", example="xxx")
    name: str = Field(..., description="connection name", example="xxx")
    payload: Dict[str, List[ConnectionPayload]] = Field(..., description="connection payload")
    referenceId: int = Field(..., description="n8n中workflow的id", example=1)
    createTime: str = Field(..., description="创建时间", example="xxx")
    updateTime: str = Field(..., description="更新时间", example="xxx")


class InputSchema(BaseModel):
    id: str = Field(..., description="schema id", example="xxx")
    info: dict = Field(..., description="json schema", example={})
    connectionId: str = Field(..., description="绑定的connection id", example="xxx")
    createTime: str = Field(..., description="创建时间", example="xxx")
    updateTime: str = Field(..., description="更新时间", example="xxx")


class ConnectionEntity(BaseModel):
    connection: Connection = Field(..., description="connection entity")
    schemaInfo: Optional[InputSchema] = Field(default=None, description="schema entity")
    active: bool = Field(..., description="is connection active", example=True)


class ConnectionResponse(BaseResponse):
    result: Optional[ConnectionEntity] = Field(default=None, description="connection entity result")


class MultipleConnectionResponse(BaseResponse):
    result: Optional[List[ConnectionEntity]] = Field(default=None, description="connection entity result")
