from typing import List, Dict
from pydantic import BaseModel, Field


class ConnectionEntity(BaseModel):
    node: str = Field(..., description="node name")


class Connection(BaseModel):
    main: List[List[ConnectionEntity]] = Field(..., description="connection entities")


class Node(BaseModel):
    parameters: dict = Field(..., description="node params", example={})
    id: str = Field(..., description="node id", example="xxx")
    type: str = Field(..., description="node type", example="xxx")
    name: str = Field(..., description="node name")
    retryOnFail: bool = Field(default=False, description="失败重试", example=False)
    maxTries: int = Field(default=0, description="重试次数", example=1)
    waitBetweenTries: int = Field(default=0, description="重试间隔", example=2000)
    continueOnFail: bool = Field(default=False, description="失败是否继续", example=True)


class Flow(BaseModel):
    nodes: List[Node] = Field(..., description="node")
    connections: Dict[str, Connection] = Field(..., description="connections")
