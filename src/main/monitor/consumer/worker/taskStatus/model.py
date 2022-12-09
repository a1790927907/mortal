from pydantic import Field
from typing import Optional
from src.main.monitor.operator.taskStatus.model import SaveTaskStatusRequestInfo as BaseSaveTaskStatusRequestInfo


class SaveTaskStatusRequestInfo(BaseSaveTaskStatusRequestInfo):
    output: Optional[dict] = Field(default=None, description="task out put", example={})
