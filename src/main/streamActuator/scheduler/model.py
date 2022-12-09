from uuid import uuid4
from typing_extensions import Literal
from pydantic import BaseModel, Field
from typing import List, Optional, Any
from src.main.streamActuator.model import Task, Connection


class TaskStatus(BaseModel):
    id: str = Field(..., description="task id", example="xxx")
    name: str = Field(..., description="task name", example="xxx")
    status: Literal['success', 'failedAndContinue', 'pending', 'skip', 'failedNotContinue'] = Field(
        ..., description="task status"
    )
    errorMessage: Optional[str] = Field(default=None, description="error message if exists", example="xxx")


class Record(BaseModel):
    require: bool = Field(default=False, description="是否需要记录日志", example=False)
    tasksRunOpenid: str = Field(default_factory=lambda: uuid4().__str__(), description="tasks run id", example="xxx")
    tasksRunningId: str = Field(
        default_factory=lambda: uuid4().__str__(), description="tasks running id", example="xxx"
    )


class ExecutionParameters(BaseModel):
    connection: Connection = Field(..., description="connection")
    tasks: List[Task] = Field(..., description="all tasks")
    context: dict = Field(default={}, description="上下文返回值记录", example={})
    taskStatus: List[TaskStatus] = Field(default=[], description="task status")
    input: dict = Field(default={}, description="入参", example={})
    record: Optional[Record] = Field(default_factory=lambda: Record(), description="日志记录相关")


class Condition(BaseModel):
    factor: Literal['eq', 'gt', 'lt', 'gte', 'lte', 'in', 'is'] = Field(default="eq", description="条件", example="eq")
    value: Any = Field(..., description="value", example="xxx")


class ExecutionCondition(BaseModel):
    type: Literal['status', 'if', 'nowait', 'wait'] = Field(default="status", description="类型", example="status")
    condition: Condition = Field(default=None, description="condition")


class Upstream(BaseModel):
    task: Task = Field(..., description="上游task")
    executionCondition: ExecutionCondition = Field(..., description="execution condition")


class ToBeExecutedTask(BaseModel):
    upstreams: List[Upstream] = Field(..., description="上游信息")
    task: Task = Field(..., description="当前task")
