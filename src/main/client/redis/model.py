from pydantic import BaseModel, Field


class JsonSchemaModelPath(BaseModel):
    path: str = Field(..., description="file path", example="xxx")
    filename: str = Field(..., description="file name", example="xxx")


class TasksRunningMapping(BaseModel):
    tasksRunId: str = Field(..., description="mapping tasks run id", example="xxx")
