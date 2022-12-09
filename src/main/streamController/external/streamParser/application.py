import json
import aiohttp

from src.main.streamController.exception import StreamControllerException
from src.main.streamController.external.streamParser.model import RequestInfo
from src.main.streamController.base.application import Application as BaseApplication


class Application(BaseApplication):
    @staticmethod
    async def _parse_stream_response_callback(res: aiohttp.ClientResponse):
        result = await res.text()
        return res.status, result

    async def _parse_stream(self, request_info: RequestInfo):
        status, response = await self.settings.session.post(
            self.settings.stream_parser_n8n_url, json=request_info.dict(),
            func=self._parse_stream_response_callback, ssl=False, timeout=300
        )
        if status != 200:
            raise StreamControllerException("解析流出错, status: {}, response: {}".format(status, response))
        response = json.loads(response)
        return response["result"]

    async def parse_stream(self, request_info: dict) -> dict:
        request_info = RequestInfo(**request_info)
        result = await self._parse_stream(request_info)
        return result
