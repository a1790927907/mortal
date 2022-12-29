from typing import List, Dict, Any
from src.main.utils.time_utils import get_now_string
from src.main.client.redis.application import application as redis_app
from src.main.streamController.exception import StreamControllerException
from src.main.utils.data_process_utils import format_dict_to_be_json_serializable
from src.main.streamController.external.application import application as external_app
from src.main.streamController.operator.loader.monitor.base.application import Application as BaseApplication


class Application(BaseApplication):
    @staticmethod
    def convert_status_payload_2_task_status(payloads: List[dict], context: dict):
        result, now = [], get_now_string()
        for payload in payloads:
            task_status = {
                "id": "auto-generate", "status": payload["status"], "runId": "auto-generate", "taskId": payload["id"],
                "errorMessage": payload["errorMessage"], "createTime": now, "updateTime": now,
                "retryTime": payload["retryTime"], "startTime": payload["startTime"], "endTime": payload["endTime"]
            }
            context_info = context.get(payload["name"]) or {}
            task_status["executeTime"] = context_info.get("executeTime") or None
            result.append(task_status)
        return result

    @staticmethod
    async def _fetch_tasks_running_by_id(tasks_running_id: str):
        tasks_running_entity = await external_app.monitor_app.get_tasks_running_by_id(tasks_running_id)
        if tasks_running_entity is None:
            raise StreamControllerException("tasks running id: {} 不存在".format(tasks_running_id), error_code=404)
        return tasks_running_entity

    @staticmethod
    def supplement_tasks_running_result_context(
            tasks_running_result: Dict[str, List[dict]], context: Dict[str, Dict[str, Any]]
    ):
        for key, values in tasks_running_result.items():
            for value in values:
                task = value["task"]
                if task["name"] in context:
                    task_output = context[task["name"]]
                    value["context"] = {"data": task_output["value"], "extra": task_output["extraValue"]}
                else:
                    value["context"] = None

    async def _get_tasks_running_by_id(self, tasks_running_id: str):
        tasks_running_entity = await self._fetch_tasks_running_by_id(tasks_running_id)
        connection_id = tasks_running_entity["connectionId"]
        status_payloads: List[dict] = tasks_running_entity["statusPayload"]["taskStatus"]
        context_payload: Dict[str, Dict[str, Any]] = tasks_running_entity["contextPayload"]
        all_task_status = self.convert_status_payload_2_task_status(
            status_payloads, tasks_running_entity["contextPayload"]
        )
        result = await self.generate_task_status_result(all_task_status, connection_id)
        self.supplement_tasks_running_result_context(result, context_payload)
        return result

    async def get_tasks_running_by_id(self, tasks_running_id: str):
        result = await self._get_tasks_running_by_id(tasks_running_id)
        format_dict_to_be_json_serializable(result)
        return {"result": result}

    @staticmethod
    async def _get_tasks_run_id_by_tasks_running_id(tasks_running_id: str) -> dict:
        result = await redis_app.get_tasks_running_mapping(tasks_running_id)
        if result is None:
            raise StreamControllerException(
                "tasks running id: {} 不存在 tasks run 缓存记录".format(tasks_running_id), error_code=404
            )
        return {"tasksRunId": result.tasksRunId}

    async def get_tasks_run_id_by_tasks_running_id(self, tasks_running_id: str):
        result = await self._get_tasks_run_id_by_tasks_running_id(tasks_running_id)
        return {"result": result}
