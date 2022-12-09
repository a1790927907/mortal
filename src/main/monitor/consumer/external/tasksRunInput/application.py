import aiohttp

from src.main.utils.logger import logger
from src.main.monitor.exception import MonitorException
from src.main.monitor.consumer.base.application import Application as BaseApplication
from src.main.monitor.operator.tasksRunInput.model import SaveTasksRunInputRequestInfo


class Application(BaseApplication):
    @staticmethod
    async def save_tasks_run_input_response_callback(res: aiohttp.ClientResponse):
        if res.status != 200:
            response = await res.text()
            raise MonitorException(
                "存储tasks run input失败, status: {}, response: {}".format(res.status, response), error_code=400
            )
        result = await res.json()
        return result["result"]

    async def save_tasks_run_input(self, request_info: SaveTasksRunInputRequestInfo):
        result = await self.settings.session.put(
            self.settings.save_tasks_run_input_url, json=request_info.dict(), ssl=False, timeout=120,
            func=self.save_tasks_run_input_response_callback
        )
        logger.info("存储 tasks run input {} 成功, run id: {}".format(result["id"], result["runId"]))
        return result
