from pydantic import Field
from src.main.client.redis.model import TasksRunningMapping as BaseTasksRunningMapping


class TasksRunningMapping(BaseTasksRunningMapping):
    redisKey: str = Field(..., description="redis key", example="xxx")
