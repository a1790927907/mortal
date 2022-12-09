from src.main.monitor.config import Settings
from fastapi import Response, APIRouter, Path, Query
from src.main.monitor.api.base.app import process_request
from src.main.monitor.operator.tasksRun.application import Application as TasksRunApplication
from src.main.monitor.operator.tasksRun.model import SaveTasksRunRequestInfo, SearchTasksRunRequestInfo
from src.main.monitor.api.tasksRun.model import SaveTasksRunResponse, TasksRunResponse, MultipleTasksRunResponse, \
    SearchTasksRunsResponse


router_app = APIRouter(prefix="/monitor/tasksRun", tags=["tasksRun"])
app = TasksRunApplication(Settings)


@router_app.post(
    "/store/save", response_model=SaveTasksRunResponse, name="创建一个tasks run记录", description="创建一个tasks run记录"
)
async def save_tasks_run(response: Response, request_info: SaveTasksRunRequestInfo):
    result = await process_request(response, coroutine=app.save_tasks_run(request_info))
    return result


@router_app.post(
    "/store/save/{tasks_run_id}", response_model=SaveTasksRunResponse, name="指定id创建一个tasks run记录",
    description="指定id创建一个tasks run记录"
)
async def save_tasks_run(
        response: Response, request_info: SaveTasksRunRequestInfo,
        tasks_run_id: str = Path(..., description="tasks run id", example="xxx")
):
    result = await process_request(response, coroutine=app.save_tasks_run(request_info, tasks_run_id=tasks_run_id))
    return result


@router_app.get(
    "/reference/connection/{connection_id}", response_model=MultipleTasksRunResponse,
    name="根据 connection id 获取多个 tasks run 记录", description="根据 connection id 获取多个 tasks run 记录"
)
async def get_tasks_runs_by_connection_id(
        response: Response,
        connection_id: str = Path(..., description="connection id", example="xxx")
):
    result = await process_request(response, coroutine=app.get_tasks_runs_by_connection_id(connection_id))
    return result


@router_app.get(
    "/condition/openid/{openid}", response_model=MultipleTasksRunResponse,
    name="根据 openid 获取多个 tasks run 记录", description="根据 openid 获取多个 tasks run 记录"
)
async def get_tasks_runs_by_openid(
        response: Response,
        openid: str = Path(..., description="openid", example="xxx")
):
    result = await process_request(response, coroutine=app.get_tasks_runs_by_openid(openid))
    return result


@router_app.get(
    "/condition/id/{tasks_run_id}", response_model=TasksRunResponse,
    name="根据 id 获取一个 tasks run 记录", description="根据 id 获取一个 tasks run 记录"
)
async def get_tasks_runs_by_id(
        response: Response,
        tasks_run_id: str = Path(..., description="tasks run id", example="xxx")
):
    result = await process_request(response, coroutine=app.get_tasks_runs_by_id(tasks_run_id))
    return result


@router_app.post(
    "/search", response_model=SearchTasksRunsResponse, name="根据条件搜索tasks run记录",
    description="根据条件搜索tasks run记录"
)
async def search_tasks_runs(
        request_info: SearchTasksRunRequestInfo,
        response: Response,
        require_count: bool = Query(default=False, description="是否需要总数", example=False)
):
    result = await process_request(response, coroutine=app.search_tasks_run(request_info, require_count=require_count))
    return result
