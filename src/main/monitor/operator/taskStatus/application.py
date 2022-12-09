from src.main.monitor.exception import MonitorException
from src.main.monitor.database.executor.taskStatus.model import TaskStatus
from src.main.monitor.base.application import Application as BaseApplication
from src.main.monitor.operator.taskStatus.model import SaveTaskStatusRequestInfo
from src.main.monitor.database.executor.application import application as database_app
from src.main.utils.data_process_utils import format_dict_to_be_json_serializable, format_list_to_be_json_serializable


class Application(BaseApplication):
    @staticmethod
    async def upsert_task_status(request_info: SaveTaskStatusRequestInfo):
        request_info = TaskStatus(**request_info.dict())
        await database_app.task_status_app.upsert_task_status(request_info)
        return {
            "id": request_info.id, "runId": request_info.runId, "taskId": request_info.taskId,
            "status": request_info.status
        }

    async def save_task_status(self, request_info: SaveTaskStatusRequestInfo):
        result = await self.upsert_task_status(request_info)
        return {"result": result}

    @staticmethod
    async def get_task_status_by_run_id(run_id: str):
        result = await database_app.task_status_app.get_status_by_run_id(run_id)
        format_list_to_be_json_serializable(result)
        return {"result": result}

    @staticmethod
    async def get_task_status_by_id(task_status_id: str):
        result = await database_app.task_status_app.get_status_by_id(task_status_id)
        if result is None:
            raise MonitorException("task status {} 不存在".format(task_status_id), error_code=404)
        format_dict_to_be_json_serializable(result)
        return {"result": result}
