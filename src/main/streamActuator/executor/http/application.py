import json
import time
import aiohttp
import asyncio
import jmespath
import traceback

from src.main.utils.logger import logger
from src.main.streamActuator.model import Task
from src.main.streamActuator.config import Settings
from src.main.utils.data_process_utils import safe_load_json
from src.main.streamActuator.executor.http.model import Output
from src.main.streamActuator.exception import StreamActuatorException
from src.main.streamActuator.executor.base.application import Application as BaseApplication


class Application(BaseApplication):
    def _process_parameters_ui(self, ui_parameters: dict):
        params = ui_parameters.get("parameter") or []
        return {
            self._parse_raw_expressions(value["name"]): self._parse_raw_expressions(value.get("value") or "")
            for value in params if value.get("name")
        }

    def _parse_json_string(self, json_string: str) -> dict:
        json_string = json_string.replace("=", "", 1) if json_string.startswith("=") else json_string
        json_string = self._parse_json_string_expressions(json_string)
        obj: dict = json.loads(json_string)
        return obj

    def process_task_parameters(self) -> Output:
        parameters = self.task.payload.parameters
        timeout = jmespath.search("options.timeout", parameters)
        result = {"method": "get".upper()}
        if timeout:
            result["timeout"] = int(timeout / 1000)
        if "url" in parameters:
            result["url"] = self._parse_raw_expressions(parameters["url"])
        if "requestMethod" in parameters:
            result["method"] = self._parse_raw_expressions(parameters["requestMethod"])
        if "bodyParametersJson" in parameters:
            result["body"] = self._parse_json_string(parameters["bodyParametersJson"])
        if "headerParametersJson" in parameters:
            result["headers"] = self._parse_json_string(parameters["headerParametersJson"])
        if "queryParametersJson" in parameters:
            result["params"] = self._parse_json_string(parameters["queryParametersJson"])
        if "headerParametersUi" in parameters:
            result["headers"] = self._parse_dict(self._process_parameters_ui(parameters["headerParametersUi"]))
        if "bodyParametersUi" in parameters:
            result["data"] = self._parse_dict(self._process_parameters_ui(parameters["bodyParametersUi"]))
        if "queryParametersUi" in parameters:
            result["params"] = self._parse_dict(self._process_parameters_ui(parameters["queryParametersUi"]))
        if "responseFormat" in parameters:
            result["response"] = {"format": parameters["responseFormat"]}
        if "dataPropertyName" in parameters:
            property_name = self._parse_raw_expressions(parameters["dataPropertyName"])
            if "response" in result:
                result["response"]["propertyName"] = property_name
            else:
                result["response"] = {"propertyName": property_name}
        if "retryOnFail" in parameters and parameters["retryOnFail"]:
            result["retry"] = {}
            if "maxTries" in parameters:
                result["retry"]["retryTime"] = parameters["maxTries"]
            if "waitBetweenTries" in parameters:
                result["retry"]["retryInterval"] = int(parameters["waitBetweenTries"] / 1000)
        result["continueOnFailed"] = parameters.get("continueOnFail", False)
        return Output(**result)

    async def _execute_task(self, parameters: Output):
        try:
            async with aiohttp.ClientSession() as session:
                # TODO: timeout 支持无上限
                res = await session.request(
                    parameters.method.lower(), parameters.url, data=parameters.data, json=parameters.body,
                    params=parameters.params, headers=parameters.headers, timeout=parameters.timeout, ssl=False
                )
                if res.status != 200:
                    response = await res.text()
                    message = "请求 {} 失败 status: {} response: {}".format(res.url.human_repr(), res.status, response)
                    self.error_message = message
                    result = safe_load_json(response, return_when_error=response)
                    self.set_result({"value": result, "extraValue": {"status": res.status, "url": res.url.human_repr()}})
                    return False
                if parameters.response.format == "json":
                    result = await res.json()
                else:
                    response = await res.text()
                    result = {
                        parameters.response.propertyName: response
                    }
                self.set_result({"value": result, "extraValue": {"status": res.status, "url": res.url.human_repr()}})
        except Exception as _e:
            logger.exception(_e)
            self.set_result({"value": None})
            self.error_message = traceback.format_exc()
            return False
        return True

    async def execute_task(self) -> bool:
        parameters = self.process_task_parameters()
        request_time = parameters.retry.retryTime if parameters.retry is not None else 1
        now = time.time()
        for i in range(request_time):
            is_success = await self._execute_task(parameters)
            if is_success is True:
                self.merge_result({"executeTime": time.time() - now})
                return is_success
            if parameters.retry is not None and i < request_time - 1:
                logger.warning("任务: {} 即将重试第 {} 次".format(self.task.name, i + 1))
                await asyncio.sleep(parameters.retry.retryInterval)
        self.merge_result({"executeTime": time.time() - now})
        raise StreamActuatorException(self.error_message, error_code=400)


def get_app(task: dict, context: dict):
    return Application(Settings, Task(**task), context)


if __name__ == '__main__':
    with open("/Users/zyh/mortal/src/main/streamActuator/executor/test/data/processed_flow.json") as f:
        print(get_app(json.load(f)["nodes"][2], {"Start": {"openId": "sadj"}}).process_task_parameters())
