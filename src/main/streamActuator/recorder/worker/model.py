from typing_extensions import Literal
from pydantic import BaseModel, Field


class QueueMessage(BaseModel):
    type: Literal['saveTaskStatus', 'saveTasksRun', 'saveTasksRunning', 'deleteTasksRunning'] = Field(
        ..., description="message type", example="saveTaskStatus"
    )
    message: dict = Field(..., description="message info", example={})
