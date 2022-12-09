from typing import Optional, List
from pydantic import BaseModel, Field
from src.main.streamController.frame.response.model import BaseResponse
from src.main.streamController.api.loader.connection.model import Connection


class TaskPayload(BaseModel):
    parameters: dict = Field(..., description="task参数", example={})


class Task(BaseModel):
    id: str = Field(..., description="connection id", example="xxx")
    name: str = Field(..., description="task name", example="xxx")
    type: str = Field(..., description="task type", example="xxx")
    payload: TaskPayload = Field(..., description="task payload")
    connectionId: str = Field(..., description="对应connection的id", example="xxx")
    createTime: str = Field(..., description="create time", example="xxx")
    updateTime: str = Field(..., description="update time", example="xxx")


class GroupedTask(BaseModel):
    inExecution: List[Task] = Field(..., description="需要执行的tasks")
    outExecution: List[Task] = Field(..., description="不需要执行的tasks")


class TaskEntity(BaseModel):
    tasks: GroupedTask = Field(..., description="排序过的tasks")
    connection: Connection = Field(..., description="binding connection")


class TaskResponse(BaseResponse):
    result: Optional[TaskEntity] = Field(default=None, description="task response")


class MultipleTaskResponse(BaseResponse):
    result: Optional[List[TaskEntity]] = Field(default=None, description="multiple task response")
