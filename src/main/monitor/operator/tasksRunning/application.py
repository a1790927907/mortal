from typing import Optional
from src.main.monitor.exception import MonitorException
from src.main.monitor.base.application import Application as BaseApplication
from src.main.monitor.operator.tasksRunning.model import SaveTasksRunningRequestInfo
from src.main.monitor.database.executor.application import application as database_app
from src.main.monitor.database.executor.tasksRunning.model import TasksRunning as DatabaseTasksRunning
from src.main.utils.data_process_utils import format_dict_to_be_json_serializable, format_list_to_be_json_serializable


class Application(BaseApplication):
    @staticmethod
    async def upsert_tasks_running(
            request_info: SaveTasksRunningRequestInfo, *, tasks_running_id: Optional[str] = None
    ):
        request_info = DatabaseTasksRunning(**request_info.dict())
        if tasks_running_id is not None:
            request_info.id = tasks_running_id
        await database_app.tasks_running_app.upsert_tasks_running(request_info)
        return {"id": request_info.id, "connectionId": request_info.connectionId}

    async def _save_tasks_running(
            self, request_info: SaveTasksRunningRequestInfo, *, tasks_running_id: Optional[str] = None
    ):
        result = await self.upsert_tasks_running(request_info, tasks_running_id=tasks_running_id)
        return result

    async def save_tasks_running(
            self, request_info: SaveTasksRunningRequestInfo, *, tasks_running_id: Optional[str] = None
    ):
        result = await self._save_tasks_running(request_info, tasks_running_id=tasks_running_id)
        return {"result": result}

    @staticmethod
    async def _get_tasks_running_by_id(tasks_running_id: str):
        result = await database_app.tasks_running_app.get_tasks_running_by_id(tasks_running_id)
        if result is None:
            raise MonitorException("tasks running id {} 不存在".format(tasks_running_id), error_code=404)
        return result

    async def get_tasks_running_by_id(self, tasks_running_id: str):
        result = await self._get_tasks_running_by_id(tasks_running_id)
        format_dict_to_be_json_serializable(result)
        return {"result": result}

    @staticmethod
    async def _get_tasks_running_by_connection_id(connection_id: str):
        result = await database_app.tasks_running_app.get_tasks_running_by_connection_id(connection_id)
        return result

    async def get_tasks_running_by_connection_id(self, connection_id: str):
        result = await self._get_tasks_running_by_connection_id(connection_id)
        format_list_to_be_json_serializable(result)
        return {"result": result}

    async def delete_tasks_running_by_id(self, tasks_running_id: str):
        await self._get_tasks_running_by_id(tasks_running_id)
        await database_app.tasks_running_app.delete_tasks_running_by_id(tasks_running_id)
        return {"result": {"id": tasks_running_id}}
