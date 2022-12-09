import aiohttp

from src.main.utils.logger import logger
from src.main.monitor.exception import MonitorException
from src.main.monitor.consumer.worker.tasksRun.model import SaveTasksRunRequestInfo
from src.main.monitor.consumer.base.application import Application as BaseApplication


class Application(BaseApplication):
    @staticmethod
    async def save_tasks_run_response_callback(res: aiohttp.ClientResponse):
        if res.status != 200:
            response = await res.text()
            raise MonitorException("存储 任务运行记录 失败, status: {}, response: {}".format(
                res.status, response
            ), error_code=400)
        result = await res.json()
        return result["result"]

    async def save_tasks_run(self, request_info: SaveTasksRunRequestInfo):
        result = await self.settings.session.post(
            self.settings.save_tasks_run_url.format(tasks_run_id=request_info.id), json=request_info.dict(), ssl=False,
            func=self.save_tasks_run_response_callback, timeout=120
        )
        logger.info("存储 tasks run {} 成功, 对应 connection id 为 {}, openid {}".format(
            result["id"], result["connectionId"], result["openid"]
        ))
