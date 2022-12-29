import os
import time
import asyncio
import traceback

from pydoc import importfile
from pydantic import BaseModel
from jsonschema import validate
from src.main.utils.logger import logger
from typing import Type, Optional, List, Tuple
from pydantic.error_wrappers import ValidationError
from src.main.streamController.exception import StreamControllerException
from src.main.client.redis.application import application as redis_application
from src.main.streamController.base.application import Application as BaseApplication
from src.main.streamController.external.application import application as external_app
from src.main.streamController.operator.trigger.model import RequestInfo, RestartTasksRunRequestInfo


class Application(BaseApplication):
    @staticmethod
    def validate_model(request_info: RequestInfo, model: Type[BaseModel]):
        try:
            model(**request_info.input)
        except ValidationError as _e:
            raise StreamControllerException("input: {} 验证model失败, detail: {}".format(
                request_info.input, traceback.format_exc()
            ), error_code=400)

    @staticmethod
    def validate_json_schema(request_info: RequestInfo, schema: dict):
        try:
            validate(request_info.input, schema)
        except Exception as e:
            logger.error(repr(e))
            raise StreamControllerException("input: {} 验证json schema失败, detail: {}".format(
                request_info.input, traceback.format_exc()
            ), error_code=400)

    @staticmethod
    async def get_model(path: str, schema_title: str) -> Optional[Type[BaseModel]]:
        loop = asyncio.get_running_loop()
        module = await loop.run_in_executor(None, importfile, path)
        model = getattr(module, schema_title, None)
        return model

    async def _validate_schema(self, request_info: RequestInfo, schema_id: str, schema: dict):
        redis_cache_info = await redis_application.get_schema_model_cache(schema_id)
        if redis_cache_info is None:
            self.validate_json_schema(request_info, schema)
        else:
            filename = redis_cache_info.filename
            path = os.path.join(redis_application.settings.model_cache_dir, filename)
            model = await self.get_model(path, schema.get("title") or "Model")
            if model is None:
                self.validate_json_schema(request_info, schema)
            else:
                self.validate_model(request_info, model)

    async def is_trigger_valid(self, request_info: RequestInfo):
        schema = await external_app.storage_app.get_schema_by_connection_id(request_info.connectionId)
        if schema is None:
            raise StreamControllerException(
                "请保证 connection {} 的input有schema".format(request_info.connectionId), error_code=400
            )
        await self._validate_schema(request_info, schema["id"], schema["info"])

    @staticmethod
    async def get_connection_by_connection_id(connection_id):
        connection = await external_app.storage_app.get_connection_by_connection_id(connection_id)
        if connection is None:
            raise StreamControllerException("connection {} 不存在".format(connection_id), error_code=404)
        return connection

    async def _trigger_connection(
            self, request_info: RequestInfo, *, connection: Optional[dict] = None, tasks: Optional[List[dict]] = None
    ):
        connection_id = request_info.connectionId
        now = time.time()
        if connection is None:
            connection = await self.get_connection_by_connection_id(connection_id)
        if tasks is None:
            tasks = await external_app.storage_app.get_tasks_by_connection(connection_id)
        storage_consuming = time.time() - now
        now = time.time()
        last_execution_info = request_info.lastExecutionInfo
        result = await external_app.actuator_app.execute_connection({
            "input": request_info.input, "connection": connection, "tasks": tasks, "record": request_info.record.dict(),
            "taskStatus": [
                status.dict() for status in last_execution_info.taskStatus
            ] if last_execution_info is not None else None,
            "context": last_execution_info.context if last_execution_info is not None else None
        })
        actuator_consuming = time.time() - now
        logger.info("执行流耗时 {}秒".format(actuator_consuming))
        return {
            "timeCost": {"actuator": actuator_consuming, "storage": storage_consuming},
            "actuatorResult": result
        }

    async def trigger_connection(self, request_info: RequestInfo):
        now = time.time()
        await self.is_trigger_valid(request_info)
        result = await self._trigger_connection(request_info)
        consuming_time = time.time() - now
        time_cost = {**result["timeCost"], "all": consuming_time}
        actuator_result = result["actuatorResult"]
        logger.info("执行完毕, 共耗时 {}秒".format(consuming_time))
        return {"result": {"timeCost": time_cost, "actuatorResult": actuator_result}}

    async def trigger_connection_asynchronous(self, request_info: RequestInfo):
        await self.is_trigger_valid(request_info)
        asyncio.create_task(self._trigger_connection(request_info))
        return {"result": None}

    @staticmethod
    async def get_tasks_run_and_input_by_run_id(run_id: str) -> Tuple[dict, dict]:
        tasks_run_entity = await external_app.monitor_app.get_tasks_run_by_run_id(run_id)
        if tasks_run_entity is None:
            raise StreamControllerException("tasks run: {} 不存在".format(run_id), error_code=404)
        tasks_run_input_entity = await external_app.monitor_app.get_tasks_run_input_by_tasks_run_id(run_id)
        if tasks_run_input_entity is None:
            raise StreamControllerException("tasks run: {} 不存在 input".format(run_id), error_code=404)
        return tasks_run_entity, tasks_run_input_entity

    async def _restart_tasks_run(self, request_info: RestartTasksRunRequestInfo):
        tasks_run_entity, tasks_run_input_entity = await self.get_tasks_run_and_input_by_run_id(request_info.tasksRunId)
        trigger_request_info = RequestInfo(
            input=tasks_run_input_entity["input"], connectionId=tasks_run_entity["connectionId"],
            record=request_info.record, asynchronous=request_info.asynchronous
        )
        if trigger_request_info.asynchronous:
            result = await self.trigger_connection_asynchronous(trigger_request_info)
        else:
            result = await self.trigger_connection(trigger_request_info)
        return result

    async def restart_tasks_run(self, request_info: RestartTasksRunRequestInfo):
        result = await self._restart_tasks_run(request_info)
        return result
