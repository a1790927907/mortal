from typing import Optional
from src.main.utils.logger import logger
from src.main.streamActuator.config import Settings
from src.main.streamActuator.recorder.base.application import Application as BaseApplication
from src.main.streamActuator.recorder.monitor.model import TaskStatusRequestInfo, TasksRunningRequestInfo, \
    TasksRunRequestInfo


class Application(BaseApplication):
    async def save_tasks_running(self, request_info: TasksRunningRequestInfo, *, partition: Optional[int] = None):
        await self.produce_message(
            self.settings.kafka_monitor_tasks_running_worker_topic, request_info.dict(), partition=partition
        )
        logger.info("发送 创建/更新 tasks running {} 任务 至 topic {} 成功, partition: {}".format(
            request_info.id, self.settings.kafka_monitor_tasks_running_worker_topic, partition
        ))

    async def delete_tasks_running(self, tasks_running_id: str, *, partition: Optional[int] = None):
        await self.produce_message(
            self.settings.kafka_monitor_tasks_running_worker_topic, {"id": tasks_running_id, "type": "delete"},
            partition=partition
        )
        logger.info("发送 删除 tasks running {} 任务 至 topic {} 成功, partition: {}".format(
            tasks_running_id, self.settings.kafka_monitor_tasks_running_worker_topic, partition
        ))

    async def save_tasks_run(self, request_info: TasksRunRequestInfo, *, partition: Optional[int] = None):
        await self.produce_message(
            self.settings.kafka_monitor_tasks_run_worker_topic, request_info.dict(), partition=partition
        )
        logger.info("发送 创建/更新 tasks run {} openid {} 任务 至 topic {} 成功, partition: {}".format(
            request_info.id, request_info.openid, self.settings.kafka_monitor_tasks_run_worker_topic, partition
        ))

    async def save_task_status(self, request_info: TaskStatusRequestInfo, *, partition: Optional[int] = None):
        await self.produce_message(
            self.settings.kafka_monitor_task_status_worker_topic, request_info.dict(), partition=partition
        )
        logger.info("发送 创建/更新 task status(绑定run id {}) 任务 至 topic {} 成功, partition: {}".format(
            request_info.runId, self.settings.kafka_monitor_task_status_worker_topic, partition
        ))


application = Application(Settings)
