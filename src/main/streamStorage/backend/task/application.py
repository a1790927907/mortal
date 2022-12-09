from typing import Union, Optional
from src.main.streamStorage.exception import StreamStorageException
from src.main.streamStorage.base.application import Application as BaseApplication
from src.main.streamStorage.database.executor.task.model import Task as DatabaseTask
from src.main.streamStorage.database.executor.application import application as database_app
from src.main.streamStorage.backend.task.model import CreateTaskRequestInfo, UpdateTaskRequestInfo
from src.main.utils.data_process_utils import format_list_to_be_json_serializable, format_dict_to_be_json_serializable


class Application(BaseApplication):
    @staticmethod
    async def upsert_task(request_info: DatabaseTask):
        await database_app.task_app.upsert_task(request_info)
        return {"id": request_info.id, "name": request_info.name}

    async def create_task(self, request_info: CreateTaskRequestInfo):
        request_info = DatabaseTask(**request_info.dict())
        result = await self.upsert_task(request_info)
        return result

    @staticmethod
    async def _get_task_by_id(task_id: str):
        task = await database_app.task_app.get_task_by_id(task_id=task_id)
        if task is None:
            raise StreamStorageException("task {} 不存在".format(task_id), error_code=404)
        return task

    async def get_task_by_id(self, task_id: str):
        result = await self._get_task_by_id(task_id)
        format_dict_to_be_json_serializable(result)
        return {"result": result}

    async def update_task(self, request_info: UpdateTaskRequestInfo, task_id: str):
        task = await self.get_task_by_id(task_id)
        request_info = {key: value for key, value in request_info.dict().items() if value is not None}
        request_info = {**task, **request_info}
        request_info.pop("updateTime", None)
        request_info = DatabaseTask(**request_info)
        result = await self.upsert_task(request_info)
        return result

    async def _save_task(
            self, request_info: Union[CreateTaskRequestInfo, UpdateTaskRequestInfo], *, task_id: Optional[str] = None
    ):
        if task_id is None:
            result = await self.create_task(request_info)
        else:
            result = await self.update_task(request_info, task_id)
        return {"result": result}

    async def save_task(
            self, request_info: Union[CreateTaskRequestInfo, UpdateTaskRequestInfo], *, task_id: Optional[str] = None
    ):
        result = await self._save_task(request_info, task_id=task_id)
        return result

    async def save_task_by_id(self, request_info: CreateTaskRequestInfo, task_id: str):
        request_info = DatabaseTask(**request_info.dict())
        request_info.id = task_id
        result = await self.upsert_task(request_info)
        return {"result": result}

    @staticmethod
    async def get_tasks_by_connection_id(connection_id: str):
        result = await database_app.task_app.get_tasks_by_connection_id(connection_id)
        format_list_to_be_json_serializable(result)
        return {"result": result}
