import aiohttp

from typing import Optional, List
from src.main.utils.logger import logger
from src.main.streamController.exception import StreamControllerException
from src.main.streamController.base.application import Application as BaseApplication
from src.main.streamController.external.streamStorage.model import SaveTaskRequestInfo, SaveConnectionRequestInfo


class Application(BaseApplication):
    @staticmethod
    async def get_connection_by_reference_id_response_callback(res: aiohttp.ClientResponse):
        if res.status == 404:
            return
        elif res.status != 200:
            response = await res.text()
            raise StreamControllerException("获取connection失败, status: {}, url: {}, response: {}".format(
                res.status, res.url.human_repr(), response
            ), error_code=400)
        result = await res.json()
        return result["result"]

    async def get_connection_by_connection_id(self, connection_id: str):
        connection = await self.settings.session.get(
            self.settings.get_stream_connection_url.format(connection_id=connection_id),
            func=self.get_connection_by_reference_id_response_callback, ssl=False, timeout=120
        )
        return connection

    async def get_connection_by_reference_id(self, reference_id: str) -> Optional[dict]:
        connection = await self.settings.session.get(
            self.settings.get_stream_connection_by_reference_url.format(reference_id=reference_id),
            func=self.get_connection_by_reference_id_response_callback, ssl=False, timeout=120
        )
        return connection

    @staticmethod
    async def upsert_connection_response_callback(res: aiohttp.ClientResponse):
        if res.status != 200:
            response = await res.text()
            raise StreamControllerException(
                "存储流失败, status: {}, response: {}".format(res.status, response), error_code=400
            )
        result = await res.json()
        return result["result"]

    async def _upsert_connection(self, request_info: SaveConnectionRequestInfo):
        connection = await self.get_connection_by_reference_id(str(request_info.referenceId))
        params = None
        if connection is not None:
            params = {"connection_id": connection["id"]}
        result = await self.settings.session.put(
            self.settings.save_stream_connection_url, json=request_info.dict(), params=params,
            func=self.upsert_connection_response_callback, ssl=False, timeout=120
        )
        logger.info("存储流 {} 成功, reference id: {}".format(result["id"], request_info.referenceId))
        return result["id"]

    async def upsert_connection(self, request_info: dict) -> str:
        request_info = SaveConnectionRequestInfo(**request_info)
        result = await self._upsert_connection(request_info)
        return result

    @staticmethod
    async def get_task_by_id_response_callback(res: aiohttp.ClientResponse):
        if res.status == 404:
            return
        elif res.status != 200:
            response = await res.text()
            raise StreamControllerException("获取task失败, status: {}, url: {}, response: {}".format(
                res.status, res.url.human_repr(), response
            ), error_code=400)
        result = await res.json()
        return result["result"]

    async def get_task_by_id(self, task_id: str) -> Optional[dict]:
        result = await self.settings.session.get(
            self.settings.get_stream_task_url.format(task_id=task_id),
            func=self.get_task_by_id_response_callback, ssl=False, timeout=120
        )
        return result

    @staticmethod
    async def delete_task_by_id_response_callback(res: aiohttp.ClientResponse):
        if res.status != 200:
            response = await res.text()
            raise StreamControllerException("删除task失败, status: {}, url: {}, response: {}".format(
                res.status, res.url.human_repr(), response
            ), error_code=400)
        result = await res.json()
        return result["result"]

    async def delete_task_by_id(self, task_id: str):
        result = await self.settings.session.delete(
            self.settings.delete_stream_task_url.format(task_id=task_id), ssl=False, timeout=120,
            func=self.delete_task_by_id_response_callback
        )
        logger.info("删除 task {} 成功, id: {}".format(result["name"], result["id"]))

    @staticmethod
    async def upsert_task_response_callback(res: aiohttp.ClientResponse):
        if res.status != 200:
            response = await res.text()
            raise StreamControllerException(
                "存储任务失败, status: {}, response: {}".format(res.status, response), error_code=400
            )
        result = await res.json()
        return result["result"]

    async def _upsert_task(self, request_info: SaveTaskRequestInfo):
        body = request_info.dict()
        task_id = body.pop("taskId")
        result = await self.settings.session.put(
            self.settings.save_stream_task_url.format(task_id=task_id), json=request_info.dict(), ssl=False,
            func=self.upsert_task_response_callback, timeout=120
        )
        logger.info("存储任务 {} 成功, connection id: {}".format(result["id"], request_info.connectionId))
        return result["id"]

    async def upsert_task(self, request_info: dict):
        request_info = SaveTaskRequestInfo(**request_info)
        await self._upsert_task(request_info)

    @staticmethod
    async def get_tasks_by_connection_response_callback(res: aiohttp.ClientResponse):
        if res.status != 200:
            response = await res.text()
            raise StreamControllerException("根据connection获取tasks失败, status: {}, url: {}, response: {}".format(
                res.status, res.url.human_repr(), response
            ), error_code=400)
        result = await res.json()
        return result["result"]

    async def get_tasks_by_connection(self, connection_id: str) -> List[dict]:
        result = await self.settings.session.get(
            self.settings.get_stream_tasks_by_connection_url.format(connection_id=connection_id),
            func=self.get_tasks_by_connection_response_callback, ssl=False, timeout=120
        )
        return result

    @staticmethod
    async def get_schema_response_callback(res: aiohttp.ClientResponse):
        if res.status == 404:
            return
        elif res.status != 200:
            response = await res.text()
            raise StreamControllerException("获取schema失败, url: {}, status: {}, response: {}".format(
                res.url.human_repr(), res.status, response
            ), error_code=400)
        result = await res.json()
        return result["result"]

    async def get_schema_by_connection_id(self, connection_id: str) -> Optional[dict]:
        schema = await self.settings.session.get(
            self.settings.get_stream_schema_by_connection_id_url.format(connection_id=connection_id),
            func=self.get_schema_response_callback, ssl=False, timeout=120
        )
        return schema
