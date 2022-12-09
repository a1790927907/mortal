from pydantic import BaseModel, Field


class TasksRunInput(BaseModel):
    runId: str = Field(..., description="binding tasks run id", example="xxx")
    input: dict = Field(..., description="tasks run input value", example={})
