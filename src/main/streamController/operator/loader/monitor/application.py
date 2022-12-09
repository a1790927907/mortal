import asyncio

from src.main.utils.logger import logger
from typing import List, Optional, cast, Dict
from src.main.utils.time_utils import get_now_string
from src.main.streamController.exception import StreamControllerException
from src.main.streamController.external.application import application as external_app
from src.main.streamController.operator.loader.monitor.model import GetTasksRunRequestInfo
from src.main.streamController.operator.loader.base.application import Application as BaseApplication


class Application(BaseApplication):
    @staticmethod
    async def _get_tasks_run(request_info: GetTasksRunRequestInfo):
        if request_info.openid:
            result = await external_app.monitor_app.get_tasks_run_by_connection_id_and_openid(
                request_info.connectionId, request_info.openid
            )
        else:
            result = await external_app.monitor_app.get_tasks_run_by_connection_id(request_info.connectionId)
        return result

    async def get_tasks_run(self, request_info: GetTasksRunRequestInfo):
        """
        没必要放在 controller 里面, 直接从monitor里面获取即可 考虑是否废弃这个
        :param request_info: ...
        :return:
        """
        result = await self._get_tasks_run(request_info)
        return {"result": result}

    @staticmethod
    async def _get_task_by_id(task_id: str):
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
            result[target_task["id"]] = target_tasks
        return list(result.values())

    async def generate_task_status_result(self, all_task_status: List[dict], run_id: str) -> Dict[str, List[dict]]:
        all_task_instance = await asyncio.gather(*[
            self._get_task_by_id(task_status["taskId"])
            for task_status in all_task_status
        ])
        all_task_instance = cast(List[Optional[dict]], all_task_instance)
        cache, result = {}, {}
        for task_status, task_instance in zip(all_task_status, all_task_instance):
            if task_instance is None:
                continue
            cache[task_instance["id"]] = {"taskStatus": task_status, "task": task_instance}
        all_task_instance = list(filter(lambda x: x, all_task_instance))
        tasks_run_instance = await external_app.monitor_app.get_tasks_run_by_run_id(run_id)
        assert tasks_run_instance is not None, "啥玩意儿啊这个run id {}".format(run_id)
        connection = await external_app.storage_app.get_connection_by_connection_id(tasks_run_instance["connectionId"])
        assert connection is not None, "这个run id {} 的connection没有啊我靠".format(run_id)
        tasks = await external_app.storage_app.get_tasks_by_connection(tasks_run_instance["connectionId"])
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
                        "errorMessage": "当前任务日志未记录或此任务未新增任务", "createTime": now, "updateTime": now
                    }
                    result[key].append({"task": value, "taskStatus": default_task_status})
        return result

    async def get_task_status_by_tasks_run_id(self, tasks_run_id: str):
        all_task_status = await external_app.monitor_app.get_task_status_by_tasks_run_id(tasks_run_id)
        result = await self.generate_task_status_result(all_task_status, tasks_run_id)
        return {"result": result}
