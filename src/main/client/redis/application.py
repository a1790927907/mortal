import json
import aioredis

from typing import Type, Optional
from src.main.client.config import Settings
from src.main.client.redis.model import JsonSchemaModelPath, TasksRunningMapping


class Application:
    def __init__(self, settings: Type[Settings]):
        self.settings = settings
        self.redis: Optional[aioredis.Redis] = None

    async def get_redis_client(self) -> aioredis.Redis:
        if self.redis is None:
            self.redis = await aioredis.from_url(self.settings.redis_server)
        return self.redis

    async def set_schema_model_cache(self, key: str, value: dict):
        request_info = JsonSchemaModelPath(**value)
        redis_client = await self.get_redis_client()
        await redis_client.hset(
            self.settings.json_schema_model_cache_key, key, json.dumps(request_info.dict(), ensure_ascii=False)
        )

    async def get_schema_model_cache(self, key: str) -> Optional[JsonSchemaModelPath]:
        redis_client = await self.get_redis_client()
        result = await redis_client.hget(self.settings.json_schema_model_cache_key, key)
        return JsonSchemaModelPath(**json.loads(result.decode())) if result else None

    async def set_tasks_running_mapping(self, key: str, values: dict):
        redis_client = await self.get_redis_client()
        request_info = TasksRunningMapping(**values)
        await redis_client.hset(
            self.settings.tasks_running_mapping_key, key, json.dumps(request_info.dict(), ensure_ascii=False)
        )

    async def get_tasks_running_mapping(self, key: str) -> TasksRunningMapping:
        redis_client = await self.get_redis_client()
        result = await redis_client.hget(self.settings.tasks_running_mapping_key, key)
        return TasksRunningMapping(**json.loads(result.decode())) if result is not None else None


application = Application(Settings)


if __name__ == '__main__':
    import asyncio
    print(asyncio.run(application.get_tasks_running_mapping("adasdd")))
