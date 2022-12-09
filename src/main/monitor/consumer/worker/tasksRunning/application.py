import json
import asyncio

from typing import Optional, Union
from src.main.utils.logger import logger
from aiokafka.structs import ConsumerRecord
from pydantic.error_wrappers import ValidationError
from src.main.monitor.consumer.base.application import Application as BaseApplication
from src.main.monitor.consumer.external.application import application as external_app
from src.main.monitor.consumer.worker.tasksRunning.model import SaveTasksRunningRequestInfo, \
    DeleteTasksRunningRequestInfo


class Application(BaseApplication):
    @staticmethod
    def get_request_info(message: ConsumerRecord) -> Optional[
        Union[SaveTasksRunningRequestInfo, DeleteTasksRunningRequestInfo]
    ]:
        request_info = json.loads(message.value.decode())
        if "type" in request_info and request_info["type"] == "delete":
            model = DeleteTasksRunningRequestInfo
        else:
            model = SaveTasksRunningRequestInfo
        try:
            return model(**request_info)
        except ValidationError as e:
            logger.exception(e)

    async def _save_tasks_running(self, request_info: SaveTasksRunningRequestInfo):
        sem = await self.get_sem(self.settings.kafka_monitor_tasks_running_worker_max_sem)
        async with sem:
            await external_app.tasks_running_app.save_tasks_running(request_info)

    async def save_tasks_running(self, request_info: SaveTasksRunningRequestInfo):
        try:
            await self._save_tasks_running(request_info)
        except Exception as e:
            logger.exception(e)

    async def process_message(self, message: ConsumerRecord):
        request_info = self.get_request_info(message)
        if request_info is not None:
            if isinstance(request_info, DeleteTasksRunningRequestInfo):
                await external_app.tasks_running_app.delete_tasks_running(request_info.id)
            else:
                await self.save_tasks_running(request_info)

    async def consume(self):
        topics = self.settings.kafka_monitor_tasks_running_worker_topic.split(",")
        consumer = await self.get_consumer(topics, self.settings.kafka_monitor_tasks_running_worker_group_id)
        logger.info("开始消费: {}".format(topics))
        while True:
            async for message in consumer:
                asyncio.create_task(self.process_message(message))
                await consumer.commit()
