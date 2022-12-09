import aiohttp

from src.main.utils.logger import logger
from src.main.monitor.exception import MonitorException
from src.main.monitor.consumer.base.application import Application as BaseApplication
from src.main.monitor.consumer.worker.taskStatus.model import SaveTaskStatusRequestInfo


class Application(BaseApplication):
    @staticmethod
    async def save_task_status_response_callback(res: aiohttp.ClientResponse):
        if res.status != 200:
            response = await res.text()
            raise MonitorException("存储 任务运行状态 失败, status: {}, response: {}".format(
                res.status, response
            ), error_code=400)
        result = await res.json()
        return result["result"]

    async def save_task_status(self, request_info: SaveTaskStatusRequestInfo) -> str:
        result = await self.settings.session.post(
            self.settings.save_task_status_url, json=request_info.dict(), ssl=False, timeout=120,
            func=self.save_task_status_response_callback
        )
        logger.info("存储 task status {} 成功, 对应 tasks run id 为 {}, task id {}, status {}".format(
            result["id"], result["runId"], result["taskId"], result["status"]
        ))
        return result["id"]
