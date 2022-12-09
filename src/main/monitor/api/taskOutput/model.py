from typing import Optional
from pydantic import Field, BaseModel
from src.main.monitor.frame.response.model import BaseResponse
from src.main.monitor.frame.request.taskOutput.model import TaskOutput


class TaskOutputEntity(TaskOutput):
    id: str = Field(..., description="tasks output id", example="xxx")
    createTime: str = Field(..., description="create time", example="xxx")
    updateTime: str = Field(..., description="update time", example="xxx")


class SaveTaskOutputResult(BaseModel):
    id: str = Field(..., description="tasks output id", example="xxx")
    taskStatusId: str = Field(..., description="binding task status id", example="xxx")
    taskId: str = Field(..., description="binding task id", example="xxx")


class SaveTaskOutputResponse(BaseResponse):
    result: SaveTaskOutputResult = Field(default=None, description="save task output result")


class TaskOutputResponse(BaseResponse):
    result: Optional[TaskOutputEntity] = Field(default=None, description="get one task output result")
