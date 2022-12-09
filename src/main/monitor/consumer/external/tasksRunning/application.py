import aiohttp

from src.main.utils.logger import logger
from src.main.monitor.exception import MonitorException
from src.main.monitor.consumer.base.application import Application as BaseApplication
from src.main.monitor.consumer.worker.tasksRunning.model import SaveTasksRunningRequestInfo


class Application(BaseApplication):
    @staticmethod
    async def save_tasks_running_response_callback(res: aiohttp.ClientResponse):
        if res.status != 200:
            response = await res.text()
            raise MonitorException("存储 tasks running 失败, status: {}, response: {}".format(
                res.status, response
            ), error_code=400)
        result = await res.json()
        return result["result"]

    async def save_tasks_running(self, request_info: SaveTasksRunningRequestInfo):
        result = await self.settings.session.put(
            self.settings.save_tasks_running_url.format(tasks_running_id=request_info.id),
            func=self.save_tasks_running_response_callback, ssl=False, timeout=120, json=request_info.dict()
        )
        logger.info("存储 tasks running {} 成功 对应 connection id {}".format(
            result["id"], result["connectionId"]
        ))

    @staticmethod
    async def delete_tasks_running_response_callback(res: aiohttp.ClientResponse):
        if res.status != 200:
            response = await res.text()
            raise MonitorException("删除 tasks running 失败, status: {}, response: {}".format(
                res.status, response
            ), error_code=400)
        result = await res.json()
        return result["result"]

    async def delete_tasks_running(self, tasks_running_id: str):
        result = await self.settings.session.delete(
            self.settings.delete_tasks_running_url.format(tasks_running_id=tasks_running_id),
            func=self.delete_tasks_running_response_callback, ssl=False, timeout=120
        )
        logger.info("删除 tasks running {} 成功".format(result["id"]))
