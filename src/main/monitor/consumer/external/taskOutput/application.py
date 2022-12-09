import aiohttp

from src.main.utils.logger import logger
from src.main.monitor.exception import MonitorException
from src.main.monitor.operator.taskOutput.model import SaveTaskOutputRequestInfo
from src.main.monitor.consumer.base.application import Application as BaseApplication


class Application(BaseApplication):
    @staticmethod
    async def save_task_output_response_callback(res: aiohttp.ClientResponse):
        if res.status != 200:
            response = await res.text()
            raise MonitorException("存储 任务输出 失败, status: {}, response: {}".format(
                res.status, response
            ), error_code=400)
        result = await res.json()
        return result["result"]

    async def save_task_output(self, request_info: SaveTaskOutputRequestInfo):
        result = await self.settings.session.post(
            self.settings.save_task_output_url, json=request_info.dict(), ssl=False,
            func=self.save_task_output_response_callback, timeout=120
        )
        logger.info("存储 task output {} 成功, 对应 status id 为 {}, task id {}".format(
            result["id"], result["taskStatusId"], result["taskId"]
        ))
