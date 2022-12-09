import json
import aiohttp

from src.main.streamController.exception import StreamControllerException
from src.main.streamController.base.application import Application as BaseApplication


class Application(BaseApplication):
    @staticmethod
    async def get_workflow_by_id_response_callback(res: aiohttp.ClientResponse):
        response = await res.text()
        return res.status, response

    async def get_workflow_by_id(self, workflow_id: int) -> dict:
        status, response = await self.settings.session.get(
            self.settings.n8n_get_workflow_by_id_url.format(id=workflow_id),
            func=self.get_workflow_by_id_response_callback, ssl=False, timeout=120,
            headers={"X-N8N-API-KEY": self.settings.n8n_api_key}
        )
        if status != 200:
            raise StreamControllerException("获取n8n workflow出错, id: {}, status: {}, response: {}".format(
                workflow_id, status, response
            ), error_code=400)
        result = json.loads(response)
        return result
