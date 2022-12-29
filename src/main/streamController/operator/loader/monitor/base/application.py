import asyncio

from src.main.utils.logger import logger
from typing import cast, List, Optional, Dict
from src.main.utils.time_utils import get_now_string
from src.main.streamController.exception import StreamControllerException
from src.main.streamController.external.application import application as external_app
from src.main.streamController.operator.loader.base.application import Application as BaseApplication


class Application(BaseApplication):
    @staticmethod
    async def _fetch_task_by_id(task_id: str):
        try:
            result = await external_app.storage_app.get_task_by_id(task_id)
            return result
        except StreamControllerException as e:
            logger.error(e.message)

    @staticmethod
    def merge_tasks(source_tasks: List[dict], target_tasks: List[dict]):
        result = {}
        for source_task in source_tasks:
            result[source_task["id"]] = source_task
        for target_task in target_tasks:
            result[target_task["id"]] = target_task
        return list(result.values())

    async def generate_task_status_result(
            self, all_task_status: List[dict], connection_id: str, *, run_id: str = "auto-generate"
    ) -> Dict[str, List[dict]]:
        all_task_instance = await asyncio.gather(*[
            self._fetch_task_by_id(task_status["taskId"])
            for task_status in all_task_status
        ])
        all_task_instance = cast(List[Optional[dict]], all_task_instance)

        cache, result, now = {}, {}, get_now_string()
        for task_status, task_instance in zip(all_task_status, all_task_instance):
            if task_instance is None:
                cache[task_status["taskId"]] = {"taskStatus": task_status, "task": {
                    "id": task_status["taskId"], "name": "已被删除的task", "type": "unknown",
                    "payload": {"parameters": {}}, "connectionId": connection_id,
                    "createTime": now, "updateTime": now
                }}
            else:
                cache[task_instance["id"]] = {"taskStatus": task_status, "task": task_instance}

        all_task_instance = [item["task"] for _, item in cache.items()]
        connection = await external_app.storage_app.get_connection_by_connection_id(connection_id)
        tasks = await external_app.storage_app.get_tasks_by_connection(connection_id)
        all_task_instance = self.merge_tasks(tasks, all_task_instance)
        ranked_tasks = self.rank_tasks(connection["payload"], all_task_instance)

        for key, values in ranked_tasks.items():
            result[key] = []
            for value in values:
                if value["id"] in cache:
                    result[key].append(cache[value["id"]])
                else:
                    now = get_now_string()
                    default_task_status = {
                        "id": "automatic-generated", "status": "none", "runId": run_id, "taskId": value["id"],
                        "errorMessage": "当前任务日志未记录或此任务为新增任务", "createTime": now, "updateTime": now,
                        "retryTime": 0
                    }
                    result[key].append({"task": value, "taskStatus": default_task_status})
        return result
