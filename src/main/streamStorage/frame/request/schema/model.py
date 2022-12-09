from pydantic import BaseModel, Field


class InputSchema(BaseModel):
    info: dict = Field(..., description="json schema", example={})
    connectionId: str = Field(..., description="绑定的connection id", example="xxx")
