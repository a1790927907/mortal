from pydantic import BaseModel, Field
from src.main.streamStorage.config import Settings


class Meta(BaseModel):
    author: str = Field(default=Settings.author, description="作者", example="zyh")
    version: str = Field(default=Settings.version, description="版本", example="1.0.0")
    description: str = Field(default=Settings.description, description="描述", example="xxx")


class BaseResponse(BaseModel):
    message: str = Field(default="ok", description="反馈信息", example="ok")
    meta: Meta = Field(default=Meta(), description="元数据")
