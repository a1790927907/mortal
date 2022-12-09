from pydantic import Field
from typing_extensions import Literal
from src.main.streamStorage.frame.request.task.model import Task, TaskPayload


class CreateTaskRequestInfo(Task):
    ...


class UpdateTaskRequestInfo(Task):
    name: str = Field(default=None, description="task name", example="xxx")
    type: Literal[
        'n8n-nodes-base.httpRequest', 'n8n-nodes-base.function', 'n8n-nodes-base.if'
    ] = Field(default=None, description="task type", example="xxx")
    payload: TaskPayload = Field(default=None, description="task payload")
    connectionId: str = Field(default=None, description="对应connection的id", example="xxx")
