from uuid import uuid4
from typing import List, Optional
from pydantic import BaseModel, Field
from src.main.streamActuator.model import Connection, Task
from src.main.streamActuator.scheduler.model import TaskStatus


class Record(BaseModel):
    require: bool = Field(default=False, description="是否需要记录日志", example=False)
    tasksRunOpenid: str = Field(default_factory=lambda: uuid4().__str__(), description="tasks run id", example="xxx")
    tasksRunningId: str = Field(
        default_factory=lambda: uuid4().__str__(), description="tasks running id", example="xxx"
    )


class Flow(BaseModel):
    connection: Connection = Field(..., description="connection")
    tasks: List[Task] = Field(..., description="nodes")
    taskStatus: Optional[List[TaskStatus]] = Field(default=None, description="task status record", example=None)
    context: Optional[dict] = Field(default=None, description="context", example=None)
    record: Optional[Record] = Field(default_factory=lambda: Record(), description="日志记录相关")


class RequestInfo(Flow):
    input: dict = Field(..., description="入参", example={})
