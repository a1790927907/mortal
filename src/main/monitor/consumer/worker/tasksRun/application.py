import json
import asyncio

from typing import Optional
from src.main.utils.logger import logger
from aiokafka.structs import ConsumerRecord
from pydantic.error_wrappers import ValidationError
from src.main.monitor.exception import MonitorException
from src.main.monitor.consumer.worker.tasksRun.model import SaveTasksRunRequestInfo
from src.main.monitor.consumer.base.application import Application as BaseApplication
from src.main.monitor.operator.tasksRunInput.model import SaveTasksRunInputRequestInfo
from src.main.monitor.consumer.external.application import application as external_app


class Application(BaseApplication):
    @staticmethod
    async def save_tasks_run_input(request_info: SaveTasksRunRequestInfo):
        await external_app.tasks_run_input_app.save_tasks_run_input(
            SaveTasksRunInputRequestInfo(runId=request_info.id, input=request_info.input)
        )

    async def _save_tasks_run(self, request_info: SaveTasksRunRequestInfo):
        sem = await self.get_sem(self.settings.kafka_monitor_tasks_run_worker_max_sem)
        async with sem:
            await external_app.tasks_run_app.save_tasks_run(request_info)
            await self.save_tasks_run_input(request_info)

    async def save_tasks_run(self, request_info: SaveTasksRunRequestInfo) -> bool:
        try:
            await self._save_tasks_run(request_info)
            return True
        except MonitorException as e:
            logger.error(e.message)
        except Exception as e:
            logger.exception(e)
        return False

    @staticmethod
    def get_request_info(message: ConsumerRecord) -> Optional[SaveTasksRunRequestInfo]:
        data = json.loads(message.value.decode())
        try:
            return SaveTasksRunRequestInfo(**data)
        except ValidationError as e:
            logger.error("验证数据结构失败...")
            logger.exception(e)

    async def process_message(self, message: ConsumerRecord):
        request_info = self.get_request_info(message)
        if request_info is not None:
            await self.save_tasks_run(request_info)

    async def consume(self):
        topics = self.settings.kafka_monitor_tasks_run_worker_topic.split(",")
        consumer = await self.get_consumer(
            topics, self.settings.kafka_monitor_tasks_run_worker_group_id
        )
        logger.info("开始消费: {}".format(topics))
        while True:
            async for msg in consumer:
                asyncio.create_task(self.process_message(msg))
                await self.consumer.commit()
