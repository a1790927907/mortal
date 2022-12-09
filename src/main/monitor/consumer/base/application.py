import asyncio

from aiokafka import AIOKafkaConsumer
from typing import Type, Optional, List
from src.main.monitor.consumer.config import Settings


class Application:
    def __init__(self, settings: Type[Settings]):
        self.settings = settings
        self.consumer: Optional[AIOKafkaConsumer] = None
        self.sem: Optional[asyncio.Semaphore] = None

    async def get_consumer(self, topics: List[str], group_id: str) -> AIOKafkaConsumer:
        if self.consumer is not None:
            return self.consumer
        self.consumer = AIOKafkaConsumer(
            *topics, bootstrap_servers=self.settings.kafka_server, group_id=group_id,
            max_poll_interval_ms=30000000000, enable_auto_commit=False, auto_offset_reset="earliest"
        )
        await self.consumer.start()
        return self.consumer

    async def get_sem(self, value: int) -> asyncio.Semaphore:
        if self.sem is None:
            self.sem = asyncio.Semaphore(value)
        return self.sem
