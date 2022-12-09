from typing import Optional
from typing_extensions import Literal
from pydantic import BaseModel, Field


class Response(BaseModel):
    format: Literal['json', 'string'] = Field(default="json", description="response format", example="json")
    propertyName: str = Field(default="data", description="返回值是个文本的时候 将会包一个property", example="data")


class Retry(BaseModel):
    retryTime: int = Field(default=3, description="重试次数", example="xxx")
    retryInterval: int = Field(default=3, description="重试间隔(s)", example=3)


class Output(BaseModel):
    url: str = Field(..., description="url", example="xxx")
    method: str = Field(..., description="request method", example="xxx")
    headers: Optional[dict] = Field(default=None, description="request headers", example={})
    body: Optional[dict] = Field(default=None, description="json body", example={})
    data: Optional[dict] = Field(default=None, description="form data", example={})
    params: Optional[dict] = Field(default=None, description="query params", example={})
    response: Response = Field(default=Response(), description="response config")
    timeout: int = Field(default=60, description="超时时间(s)", example=60)
    retry: Retry = Field(default=None, description="retry config")
    continueOnFailed: bool = Field(default=False, description="失败了是否继续执行下面的任务", example=False)
