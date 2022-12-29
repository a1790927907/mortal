import asyncio

from src.main.utils.logger import logger
from typing import Type, List, Any, Optional
from pydantic.error_wrappers import ValidationError
from src.main.streamActuator.config import Settings
from src.main.streamActuator.recorder.worker.model import QueueMessage
from src.main.streamActuator.recorder.redis.model import TasksRunningMapping
from src.main.streamActuator.recorder.redis.application import application as redis_app
from src.main.streamActuator.recorder.monitor.application import application as monitor_app
from src.main.streamActuator.recorder.base.application import Application as BaseApplication
from src.main.streamActuator.recorder.monitor.model import TaskStatusRequestInfo, TasksRunRequestInfo, \
    TasksRunningRequestInfo


class Application(BaseApplication):
    def __init__(self, settings: Type[Settings]):
        super().__init__(settings)
        self._queues: Optional[List[asyncio.Queue]] = None

    async def generate_queues(self):
        self._queues = [asyncio.Queue(maxsize=-1) for _ in range(self.settings.actuator_monitor_queue_size)]

    @staticmethod
    def _choose_queue(queue_info: List[dict]) -> asyncio.Queue:
        min_size_queue_info = min(queue_info, key=lambda x: x["size"])
        return min_size_queue_info["queue"]

    @property
    def queue(self):
        queue_info = [
            {"size": queue.qsize(), "queue": queue}
            for queue in self._queues
        ]
        return self._choose_queue(queue_info)

    @staticmethod
    def get_execution_coroutine(message: Any):
        if isinstance(message, dict):
            message = QueueMessage(**message)
        else:
            logger.error("invalid message {} -> must be a dict".format(message))
            return
        if message.type == "saveTaskStatus":
            model, coroutine = TaskStatusRequestInfo, monitor_app.save_task_status
        elif message.type == "saveTasksRun":
            model, coroutine = TasksRunRequestInfo, monitor_app.save_tasks_run
        elif message.type == "saveTasksRunning":
            model, coroutine = TasksRunningRequestInfo, monitor_app.save_tasks_running
        elif message.type == "saveTasksRunningMapping":
            return redis_app.save_tasks_running_mapping(TasksRunningMapping(**message.message))
        else:
            if "id" not in message.message:
                logger.error("删除 tasks running 时 遇到问题: message 不合法(没有id) {}".format(message.message))
                return
            return monitor_app.delete_tasks_running(message.message["id"], partition=message.messageConfig.partition)
        try:
            return coroutine(model(**message.message), partition=message.messageConfig.partition)
        except ValidationError as e:
            logger.error("操作类型: {}, 验证 request info 失败".format(message.type))
            logger.exception(e)

    async def process_message(self, message: Any):
        try:
            coroutine = self.get_execution_coroutine(message)
            if coroutine is not None:
                await coroutine
        except Exception as e:
            logger.exception(e)

    async def consume(self, queue: asyncio.Queue):
        logger.info("开始消费queue: {}".format(id(queue)))
        while True:
            message = await queue.get()
            await self.process_message(message)
            queue.task_done()

    async def init_queue_consumer(self):
        await self.generate_queues()
        logger.info("初始化 {} 组 queue: {}".format(len(self._queues), [id(q) for q in self._queues]))
        for queue in self._queues:
            asyncio.create_task(self.consume(queue))


application = Application(Settings)
