import dateutil.parser as date_parser

from datetime import datetime
from typing import Optional, cast
from src.main.monitor.exception import MonitorException
from src.main.monitor.base.application import Application as BaseApplication
from src.main.monitor.database.executor.application import application as database_app
from src.main.monitor.operator.tasksRun.model import SaveTasksRunRequestInfo, SearchTasksRunRequestInfo
from src.main.utils.data_process_utils import format_dict_to_be_json_serializable, format_list_to_be_json_serializable
from src.main.monitor.database.executor.tasksRun.model import TasksRun, SearchTasksRunRequestInfo as \
    DatabaseSearchTasksRunRequestInfo


class Application(BaseApplication):
    @staticmethod
    async def upsert_tasks_run(request_info: SaveTasksRunRequestInfo, *, tasks_run_id: Optional[str] = None):
        tasks_run = TasksRun(**request_info.dict())
        if tasks_run_id is not None:
            tasks_run.id = tasks_run_id
        await database_app.tasks_run_app.create_tasks_run(tasks_run)
        return {"id": tasks_run.id, "connectionId": tasks_run.connectionId, "openid": tasks_run.openid}

    async def create_tasks_run(self, request_info: SaveTasksRunRequestInfo, *, tasks_run_id: Optional[str] = None):
        result = await self.upsert_tasks_run(request_info, tasks_run_id=tasks_run_id)
        return result

    async def save_tasks_run(self, request_info: SaveTasksRunRequestInfo, *, tasks_run_id: Optional[str] = None):
        result = await self.create_tasks_run(request_info, tasks_run_id=tasks_run_id)
        return {"result": result}

    @staticmethod
    async def get_tasks_runs_by_connection_id(connection_id: str):
        result = await database_app.tasks_run_app.get_tasks_runs_by_connection_id(connection_id)
        format_list_to_be_json_serializable(result)
        return {"result": result}

    @staticmethod
    async def get_tasks_runs_by_openid(openid: str):
        result = await database_app.tasks_run_app.get_tasks_runs_by_openid(openid)
        format_list_to_be_json_serializable(result)
        return {"result": result}

    @staticmethod
    async def get_tasks_runs_by_id(tasks_run_id: str):
        result = await database_app.tasks_run_app.get_tasks_run_by_id(tasks_run_id)
        if result is None:
            raise MonitorException("tasks run id {} 不存在".format(tasks_run_id), error_code=404)
        format_dict_to_be_json_serializable(result)
        return {"result": result}

    @staticmethod
    def parse_date(text: str) -> datetime:
        fmt = "%Y-%m-%d %H:%M:%S"
        try:
            return datetime.strptime(date_parser.parse(text).strftime(fmt), fmt)
        except Exception as _e:
            raise MonitorException("搜索条件中的时间文本不对: {}".format(text), error_code=400)

    def process_request_info(self, request_info: SearchTasksRunRequestInfo) -> DatabaseSearchTasksRunRequestInfo:
        database_request_info = DatabaseSearchTasksRunRequestInfo(pageInfo={
            "limit": request_info.pageInfo.size, "offset": (request_info.pageInfo.page - 1) * request_info.pageInfo.size
        }, filterInfo=request_info.filterInfo, order=request_info.order, connectionId=request_info.connectionId)
        if database_request_info.filterInfo is not None:
            for filter_info in database_request_info.filterInfo:
                if filter_info.by == "updateTime" or filter_info.by == "startTime" or filter_info.by == "endTime":
                    if isinstance(filter_info.value, str):
                        filter_info.value = self.parse_date(cast(str, filter_info.value))
        return database_request_info

    async def _search_tasks_run(self, request_info: SearchTasksRunRequestInfo, *, require_count: bool = False):
        database_request_info = self.process_request_info(request_info)
        result = await database_app.tasks_run_app.search_tasks_run_by_request_info(database_request_info)
        if require_count:
            count = await database_app.tasks_run_app.get_tasks_runs_number_after_search(database_request_info)
        else:
            count = None
        return {"tasksRuns": result, "total": count}

    async def search_tasks_run(self, request_info: SearchTasksRunRequestInfo, *, require_count: bool = False):
        result = await self._search_tasks_run(request_info, require_count=require_count)
        format_dict_to_be_json_serializable(result)
        return {"result": result}
