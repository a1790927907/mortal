from uuid import uuid4
from typing import Optional, List
from typing_extensions import Literal
from pydantic import BaseModel, Field


class Record(BaseModel):
    require: bool = Field(default=False, description="是否需要记录日志", example=False)
    tasksRunOpenid: str = Field(default_factory=lambda: uuid4().__str__(), description="tasks run id", example="xxx")
    tasksRunningId: str = Field(
        default_factory=lambda: uuid4().__str__(), description="tasks running id", example="xxx"
    )


class TaskStatus(BaseModel):
    id: str = Field(..., description="task id", example="xxx")
    name: str = Field(..., description="task name", example="xxx")
    status: Literal['success', 'failedAndContinue', 'pending', 'skip', 'failedNotContinue'] = Field(
        ..., description="task status"
    )
    errorMessage: Optional[str] = Field(default=None, description="error message if exists", example="xxx")


class LastExecutionInfo(BaseModel):
    taskStatus: Optional[List[TaskStatus]] = Field(
        ..., description="任务状态记录, 如果存在这个参数的话, 执行器会根据status内容断点执行", example=[]
    )
    context: Optional[dict] = Field(..., description="任务上下文记录, 请配合taskStatus使用", example={})


class RequestInfo(BaseModel):
    input: dict = Field(..., description="input value", example={})
    connectionId: str = Field(..., description="需要触发的connection的id", example="xxx")
    record: Optional[Record] = Field(default_factory=lambda: Record(), description="日志记录相关")
    lastExecutionInfo: Optional[LastExecutionInfo] = Field(
        default=None, description="上次的执行记录信息, 一般不填写就会从头执行"
    )
