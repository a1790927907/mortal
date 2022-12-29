from typing import Optional
from typing_extensions import Literal
from pydantic import BaseModel, Field


class MessageConfig(BaseModel):
    partition: Optional[int] = Field(default=None, description="kafka消息发至哪个分区, 默认随意", example=1)


class QueueMessage(BaseModel):
    type: Literal[
        'saveTaskStatus', 'saveTasksRun', 'saveTasksRunning', 'deleteTasksRunning', 'saveTasksRunningMapping'
    ] = Field(
        ..., description="message type", example="saveTaskStatus"
    )
    message: dict = Field(..., description="message info", example={})
    messageConfig: MessageConfig = Field(default=MessageConfig(), description="kafka message config")
