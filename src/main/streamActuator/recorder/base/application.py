import json

from typing import Type, Optional
from aiokafka import AIOKafkaProducer
from src.main.streamActuator.config import Settings
from src.main.streamActuator.base.application import Application as BaseApplication


class Application(BaseApplication):
    def __init__(self, settings: Type[Settings]):
        super().__init__(settings)
        self.producer: Optional[AIOKafkaProducer] = None

    async def get_producer(self):
        if self.producer is None:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.settings.kafka_server, max_request_size=100 * 1024 * 1024
            )
            await self.producer.start()
        return self.producer

    async def produce_message(self, topic: str, message: dict):
        producer = await self.get_producer()
        await producer.send_and_wait(topic, json.dumps(message, ensure_ascii=False).encode())
