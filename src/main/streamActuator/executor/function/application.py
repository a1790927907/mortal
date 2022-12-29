import time
import inspect
import asyncio

from typing import Callable
from pydoc import importfile
from src.main.utils.logger import logger
from src.main.streamActuator.model import Task
from src.main.streamActuator.config import Settings
from src.main.utils.data_process_utils import get_multiple_value_by_keys
from src.main.streamActuator.executor.base.application import Application as BaseApplication


class Application(BaseApplication):
    @property
    def function_file_path(self):
        parameters = self.task.payload.parameters
        return parameters["path"]

    async def get_function(self) -> Callable:
        loop = asyncio.get_running_loop()
        path = self.function_file_path
        module = await loop.run_in_executor(None, importfile, path)
        func = getattr(module, "process", None)
        assert func is not None, "{} 不存在名为process的function".format(path)
        return func

    async def execute_function(self, func: Callable):
        retry, retry_time, retry_interval = get_multiple_value_by_keys(
            ["retryOnFail", "maxTries", "waitBetweenTries"], self.task.payload.parameters
        )
        retry_time = retry_time if retry is True else 1
        retry_time = retry_time or 1
        context = {key: value["value"] for key, value in self.context.items()}
        extra_kwargs = {key: value.get("extraValue") or {} for key, value in self.context.items()}
        for i in range(retry_time + 1):
            try:
                if inspect.iscoroutinefunction(func):
                    result = await func(context, **extra_kwargs)
                else:
                    result = func(context, **extra_kwargs)
                return result
            except Exception as e:
                if i < retry_time - 1:
                    logger.exception(e)
                    logger.warning("任务: {} 即将重试第 {} 次".format(self.task.name, i + 1))
                    self.retry_time += 1
                    await asyncio.sleep(retry_interval)
                else:
                    raise e

    async def execute_task(self) -> bool:
        now = time.time()
        try:
            func = await self.get_function()
            result = await self.execute_function(func)
        except Exception as _e:
            self.set_result({"value": None, "executeTime": time.time() - now})
            raise _e
        self.set_result({"value": result, "executeTime": time.time() - now})
        return True


def get_app(task: dict, context: dict):
    return Application(Settings, Task(**task), context)
