from src.main.utils.logger import logger
from src.main.client.redis.application import application as redis_app
from src.main.streamActuator.recorder.redis.model import TasksRunningMapping


class Application:
    @staticmethod
    async def save_tasks_running_mapping(request_info: TasksRunningMapping):
        await redis_app.set_tasks_running_mapping(request_info.redisKey, request_info.dict())
        logger.info("存储 tasks running id: {} mapping tasks run: {} 成功".format(
            request_info.redisKey, request_info.tasksRunId
        ))


application = Application()
