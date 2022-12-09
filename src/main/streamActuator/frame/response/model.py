from pydantic import BaseModel, Field
from src.main.streamActuator.config import Settings


class Meta(BaseModel):
    author: str = Field(default=Settings.author, description="作者", example="xxx")
    version: str = Field(default=Settings.version, description="version", example="1.0.0")
    description: str = Field(default=Settings.description, description="描述", example="xxx")


class BaseResponse(BaseModel):
    message: str = Field(default="ojbk", description="反馈信息", example="ok")
    meta: Meta = Field(default=Meta(), description="元数据")
