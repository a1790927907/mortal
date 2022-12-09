from src.main.monitor.exception import MonitorException
from src.main.monitor.database.executor.taskOutput.model import TaskOutput
from src.main.monitor.base.application import Application as BaseApplication
from src.main.monitor.operator.taskOutput.model import SaveTaskOutputRequestInfo
from src.main.utils.data_process_utils import format_dict_to_be_json_serializable
from src.main.monitor.database.executor.application import application as database_app


class Application(BaseApplication):
    @staticmethod
    async def upsert_task_output(request_info: SaveTaskOutputRequestInfo):
        request_info = TaskOutput(**request_info.dict())
        await database_app.task_output_app.save_task_output(request_info)
        return {"id": request_info.id, "taskStatusId": request_info.taskStatusId, "taskId": request_info.taskId}

    async def save_task_output(self, request_info: SaveTaskOutputRequestInfo):
        result = await self.upsert_task_output(request_info)
        return {"result": result}

    @staticmethod
    async def get_task_output_by_status_id(task_status_id: str):
        result = await database_app.task_output_app.get_task_output_by_task_status_id(task_status_id)
        if result is None:
            raise MonitorException("task status id {} 不存在 output".format(task_status_id), error_code=404)
        format_dict_to_be_json_serializable(result)
        return {"result": result}
