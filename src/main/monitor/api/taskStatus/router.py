from src.main.monitor.config import Settings
from fastapi import Response, APIRouter, Path
from src.main.monitor.api.base.app import process_request
from src.main.monitor.operator.taskStatus.model import SaveTaskStatusRequestInfo
from src.main.monitor.operator.taskStatus.application import Application as TasksStatusApplication
from src.main.monitor.api.taskStatus.model import SaveTaskStatusResponse, TaskStatusResponse, MultipleTaskStatusResponse


router_app = APIRouter(prefix="/monitor/taskStatus", tags=["taskStatus"])
app = TasksStatusApplication(Settings)


@router_app.post(
    "/store/save", response_model=SaveTaskStatusResponse, name="创建一个task status 记录",
    description="创建一个task status 记录"
)
async def save_task_status(response: Response, request_info: SaveTaskStatusRequestInfo):
    result = await process_request(response, coroutine=app.save_task_status(request_info))
    return result


@router_app.get(
    "/reference/tasksRun/{run_id}", response_model=MultipleTaskStatusResponse,
    name="根据 run id 获取多个 task status 记录", description="根据 run id 获取多个 task status 记录"
)
async def get_task_status_by_run_id(
        response: Response,
        run_id: str = Path(..., description="run id", example="xxx")
):
    result = await process_request(response, coroutine=app.get_task_status_by_run_id(run_id))
    return result


@router_app.get(
    "/condition/id/{status_id}", response_model=TaskStatusResponse,
    name="根据 id 获取单个 task status 记录", description="根据 id 获取单个 task status 记录"
)
async def get_task_status_by_id(
        response: Response,
        status_id: str = Path(..., description="status id", example="xxx")
):
    result = await process_request(response, coroutine=app.get_task_status_by_id(status_id))
    return result
