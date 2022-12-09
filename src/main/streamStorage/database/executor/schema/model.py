import uuid

from pydantic import Field
from datetime import datetime
from src.main.utils.time_utils import get_now
from src.main.streamStorage.frame.request.schema.model import InputSchema as BaseInputSchema


class InputSchema(BaseInputSchema):
    id: str = Field(default_factory=lambda: uuid.uuid4().__str__(), description="connection id", example="xxx")
    updateTime: datetime = Field(default_factory=get_now, description="更新时间", example="xxx")
