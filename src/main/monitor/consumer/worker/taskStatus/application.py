import json
import asyncio

from typing import Optional
from src.main.utils.logger import logger
from aiokafka.structs import ConsumerRecord
from pydantic.error_wrappers import ValidationError
from src.main.monitor.exception import MonitorException
from src.main.monitor.operator.taskOutput.model import SaveTaskOutputRequestInfo
from src.main.monitor.consumer.base.application import Application as BaseApplication
from src.main.monitor.consumer.external.application import application as external_app
from src.main.monitor.consumer.worker.taskStatus.model import SaveTaskStatusRequestInfo


class Application(BaseApplication):
    @staticmethod
    async def save_task_output(request_info: SaveTaskStatusRequestInfo, status_id: str):
        output_request_info = SaveTaskOutputRequestInfo(**{
            "taskStatusId": status_id, "taskId": request_info.taskId, "output": request_info.output
        })
        await external_app.task_output_app.save_task_output(output_request_info)

    async def _save_task_status(self, request_info: SaveTaskStatusRequestInfo):
        sem = await self.get_sem(self.settings.kafka_monitor_task_status_worker_max_sem)
        async with sem:
            status_id = await external_app.task_status_app.save_task_status(request_info)
            if request_info.output:
                await self.save_task_output(request_info, status_id)

    async def save_task_status(self, request_info: SaveTaskStatusRequestInfo) -> bool:
        try:
            await self._save_task_status(request_info)
            return True
        except MonitorException as e:
            logger.error(e.message)
        except Exception as e:
            logger.exception(e)
        return False

    @staticmethod
    def get_request_info(message: ConsumerRecord) -> Optional[SaveTaskStatusRequestInfo]:
        data = json.loads(message.value.decode())
        try:
            return SaveTaskStatusRequestInfo(**data)
        except ValidationError as e:
            logger.error("验证数据结构失败...")
            logger.exception(e)

    async def process_message(self, message: ConsumerRecord):
        request_info = self.get_request_info(message)
        if request_info is not None:
            await self.save_task_status(request_info)

    async def consume(self):
        topics = self.settings.kafka_monitor_task_status_worker_topic.split(",")
        consumer = await self.get_consumer(
            topics, self.settings.kafka_monitor_task_status_worker_group_id
        )
        logger.info("开始消费: {}".format(topics))
        while True:
            async for msg in consumer:
                asyncio.create_task(self.process_message(msg))
                await self.consumer.commit()
