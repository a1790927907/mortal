from typing import Optional
from src.main.monitor.exception import MonitorException
from src.main.monitor.base.application import Application as BaseApplication
from src.main.utils.data_process_utils import format_dict_to_be_json_serializable
from src.main.monitor.operator.tasksRunInput.model import SaveTasksRunInputRequestInfo
from src.main.monitor.database.executor.application import application as database_app
from src.main.monitor.database.executor.tasksRunInput.model import TasksRunInput as DatabaseTasksRunInput


class Application(BaseApplication):
    @staticmethod
    async def upsert_tasks_run_input(
            request_info: SaveTasksRunInputRequestInfo, *, tasks_run_input_id: Optional[str] = None
    ):
        request_info = DatabaseTasksRunInput(**request_info.dict())
        if tasks_run_input_id:
            request_info.id = tasks_run_input_id
        await database_app.tasks_run_input_app.save_tasks_run_input(request_info)
        return {"id": request_info.id, "runId": request_info.runId}

    async def update_tasks_run_input(self, request_info: SaveTasksRunInputRequestInfo, tasks_run_input_id: str):
        result = await self.upsert_tasks_run_input(request_info, tasks_run_input_id=tasks_run_input_id)
        return result

    async def create_tasks_run_input(self, request_info: SaveTasksRunInputRequestInfo):
        result = await self.upsert_tasks_run_input(request_info)
        return result

    @staticmethod
    async def _get_tasks_input_by_run_id(tasks_run_id: str):
        result = await database_app.tasks_run_input_app.get_tasks_run_input_by_run_id(tasks_run_id)
        return result

    async def save_tasks_run_input(self, request_info: SaveTasksRunInputRequestInfo):
        tasks_run_input = await self._get_tasks_input_by_run_id(request_info.runId)
        if tasks_run_input is None:
            result = await self.create_tasks_run_input(request_info)
        else:
            result = await self.update_tasks_run_input(request_info, tasks_run_input["id"])
        return {"result": result}

    async def get_tasks_input_by_run_id(self, tasks_run_id: str):
        result = await self._get_tasks_input_by_run_id(tasks_run_id)
        if result is None:
            raise MonitorException("tasks run id {} 不存在 input".format(tasks_run_id), error_code=404)
        format_dict_to_be_json_serializable(result)
        return {"result": result}
