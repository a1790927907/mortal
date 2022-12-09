import aiohttp

from aiokafka import AIOKafkaProducer
from typing import Type, Optional, List
from src.main.streamController.config import Settings
from src.main.streamController.exception import StreamControllerException
from src.main.streamController.base.application import Application as BaseApplication


class Application(BaseApplication):
    def __init__(self, settings: Type[Settings]):
        super().__init__(settings)
        self.producer: Optional[AIOKafkaProducer] = None

    @staticmethod
    async def _request_response_callback(res: aiohttp.ClientResponse):
        result = await res.json()
        return res.status, result

    async def get_tasks_run_by_connection_id(self, connection_id: str) -> Optional[List[dict]]:
        status, response = await self.settings.session.get(
            self.settings.get_tasks_run_by_connection_id_url.format(connection_id=connection_id),
            func=self._request_response_callback, ssl=False, timeout=120
        )
        if status != 200:
            raise StreamControllerException(
                "获取connection id {} 对应的 tasks run失败, status: {}, response: {}".format(
                    connection_id, status, response
                ), error_code=400
            )
        return response["result"]

    async def get_tasks_run_by_connection_id_and_openid(self, connection_id: str, openid: str) -> Optional[List[dict]]:
        tasks_runs_instance = await self.get_tasks_run_by_connection_id(connection_id)
        result = []
        for tasks_runs in tasks_runs_instance:
            if tasks_runs["openid"] == openid:
                result.append(tasks_runs)
        return result

    async def get_tasks_run_by_run_id(self, tasks_run_id: str) -> Optional[dict]:
        status, response = await self.settings.session.get(
            self.settings.get_tasks_run_by_id_url.format(tasks_run_id=tasks_run_id),
            func=self._request_response_callback, ssl=False, timeout=120
        )
        if status == 404:
            return
        elif status != 200:
            raise StreamControllerException(
                "获取tasks run id {} 失败, status: {}, response: {}".format(
                    tasks_run_id, status, response
                ), error_code=400
            )
        return response["result"]

    async def get_task_status_by_tasks_run_id(self, tasks_run_id: str) -> Optional[List[dict]]:
        status, response = await self.settings.session.get(
            self.settings.get_all_task_status_by_tasks_run_id.format(run_id=tasks_run_id),
            func=self._request_response_callback, ssl=False, timeout=120
        )
        if status != 200:
            raise StreamControllerException(
                "获取tasks run id {} 对应的 task status失败, status: {}, response: {}".format(
                    tasks_run_id, status, response
                ), error_code=400
            )
        return response["result"]

    async def get_tasks_run_input_by_tasks_run_id(self, tasks_run_id: str) -> Optional[dict]:
        status, response = await self.settings.session.get(
            self.settings.get_tasks_run_input_url.format(tasks_run_id=tasks_run_id),
            func=self._request_response_callback, ssl=False, timeout=120
        )
        if status != 200:
            raise StreamControllerException(
                "获取tasks run id {} 对应的 task input 失败, status: {}, response: {}".format(
                    tasks_run_id, status, response
                ), error_code=400
            )
        return response["result"]

    async def get_task_output_by_task_status_id(self, task_status_id: str):
        status, response = await self.settings.session.get(
            self.settings.get_task_output_url.format(task_status_id=task_status_id),
            func=self._request_response_callback, ssl=False, timeout=120
        )
        if status == 404:
            return
        elif status != 200:
            raise StreamControllerException(
                "获取task status id {} 对应的 task output 失败, status: {}, response: {}".format(
                    task_status_id, status, response
                ), error_code=400
            )
        return response["result"]
