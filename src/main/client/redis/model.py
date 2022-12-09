from pydantic import BaseModel, Field


class JsonSchemaModelPath(BaseModel):
    path: str = Field(..., description="file path", example="xxx")
    filename: str = Field(..., description="file name", example="xxx")
