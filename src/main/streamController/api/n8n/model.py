from pydantic import BaseModel, Field
from src.main.streamController.frame.response.model import BaseResponse


class SaveConnectionFromN8NResult(BaseModel):
    referenceId: int = Field(..., description="reference id(n8n work flow id)", example=1)
    connectionId: str = Field(..., description="connection id", example="xxx")


class SaveConnectionFromN8NResponse(BaseResponse):
    result: SaveConnectionFromN8NResult = Field(default=None, description="save connection from n8n")
