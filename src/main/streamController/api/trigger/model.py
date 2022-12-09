from pydantic import BaseModel as Bm, Field
from typing_extensions import Literal
from typing import Optional, List, Dict, Any
from src.main.streamController.frame.response.model import BaseResponse


class BaseModel(Bm):
    class Config:
        extra = "allow"


class TimeCost(BaseModel):
    actuator: float = Field(..., description="执行耗时", example=0.)
    storage: float = Field(..., description="从数据库拉取数据耗时", example=0.)
    all: float = Field(..., description="总耗时", example=0.)


class ExecutorResult(BaseModel):
    value: Any = Field(..., description="result", example="")
    extraValue: dict = Field(default={}, description="extra something", example={})
    executeTime: float = Field(default=None, description="执行时长", example=0.)


class TaskStatus(BaseModel):
    id: str = Field(..., description="task id", example="xxx")
    name: str = Field(..., description="task name", example="xxx")
    status: Literal['success', 'failedAndContinue', 'pending', 'skip', 'failedNotContinue'] = Field(
        ..., description="task status"
    )
    errorMessage: Optional[str] = Field(default=None, description="error message if exists", example="xxx")


class ActuatorResult(BaseModel):
    status: List[TaskStatus] = Field(..., description="task status")
    context: Dict[str, ExecutorResult] = Field(..., description="task execute result")
    cost: float = Field(..., description="耗时", example=0.)


class TriggerConnectionResult(BaseModel):
    timeCost: TimeCost = Field(..., description="time cost record")
    actuatorResult: ActuatorResult = Field(..., description="actuator result record")


class TriggerConnectionResponse(BaseResponse):
    result: TriggerConnectionResult = Field(default=None, description="trigger connection result")
