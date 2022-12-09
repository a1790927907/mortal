from fastapi import Query
from typing import Optional
from pydantic import BaseModel


class GetTasksRunRequestInfo(BaseModel):
    connectionId: str = Query(..., description="connection id", example="xxx")
    openid: Optional[str] = Query(default=None, description="tasks run signal openid", example="xxx")
