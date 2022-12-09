from typing import List, Dict
from pydantic import BaseModel, Field
from src.main.streamActuator.scheduler.model import TaskStatus
from src.main.streamActuator.executor.model import ExecutorResult
from src.main.streamActuator.frame.response.model import BaseResponse


class TriggerConnectionResult(BaseModel):
    status: List[TaskStatus] = Field(..., description="task status")
    context: Dict[str, ExecutorResult] = Field(..., description="task execute result")
    cost: float = Field(..., description="耗时", example=0.)


class TriggerConnectionResponse(BaseResponse):
    result: TriggerConnectionResult = Field(default=None, description="trigger connection result")
