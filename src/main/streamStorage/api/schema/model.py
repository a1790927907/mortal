from pydantic import Field, BaseModel
from src.main.streamStorage.frame.request.schema.model import InputSchema
from src.main.streamStorage.frame.response.base.model import BaseResponse


class SchemaResult(InputSchema):
    id: str = Field(..., description="schema id", example="xxx")
    createTime: str = Field(..., description="创建时间", example="xxx")
    updateTime: str = Field(..., description="更新时间", example="xxx")


class SaveSchemaResult(BaseModel):
    id: str = Field(..., description="schema id", example="xxx")
    connectionId: str = Field(..., description="connection id", example="xxx")


class SaveSchemaResponse(BaseResponse):
    result: SaveSchemaResult = Field(default=None, description="save schema result")


class GetSchemaResponse(BaseResponse):
    result: SchemaResult = Field(default=None, description="schema result")
