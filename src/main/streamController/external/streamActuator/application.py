import json
import aiohttp

from src.main.streamController.exception import StreamControllerException
from src.main.streamController.external.streamActuator.model import RequestInfo
from src.main.streamController.base.application import Application as BaseApplication


class Application(BaseApplication):
    @staticmethod
    async def _execute_connection_response_callback(res: aiohttp.ClientResponse):
        result = await res.text()
        return res.status, result

    async def _execute_connection(self, request_info: RequestInfo):
        status, response = await self.settings.session.post(
            self.settings.trigger_stream_url, json=request_info.dict(), func=self._execute_connection_response_callback,
            ssl=False
        )
        if status != 200:
            raise StreamControllerException("执行流出错, status: {}, response: {}".format(status, response))
        response = json.loads(response)
        return response["result"]

    async def execute_connection(self, request_info: dict) -> dict:
        request_info = RequestInfo(**request_info)
        result = await self._execute_connection(request_info)
        return result
