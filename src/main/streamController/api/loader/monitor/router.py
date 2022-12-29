from fastapi import APIRouter, Response, Path
from src.main.streamController.config import Settings
from src.main.streamController.api.base.app import process_request
from src.main.streamController.operator.loader.monitor.taskStatus.application import Application as \
    TaskStatusApplication
from src.main.streamController.operator.loader.monitor.tasksRunnings.application import Application as \
    TasksRunningApplication
from src.main.streamController.api.loader.monitor.model import TaskStatusLoadedResponse, \
    TasksRunningStatusLoadedResponse, TasksRunningMappingResponse


router_app = APIRouter(prefix="/stream/reference/monitor", tags=["monitor"])
task_status_app = TaskStatusApplication(Settings)
task_running_app = TasksRunningApplication(Settings)


@router_app.get(
    "/taskStatus/condition/tasksRun/{tasks_run_id}", response_model=TaskStatusLoadedResponse,
    description="根据tasks run id获取对应的task status记录", name="根据tasks run id获取对应的task status记录"
)
async def get_task_status_by_tasks_run_id(
        response: Response,
        tasks_run_id: str = Path(..., description="tasks run id", example="xxx")
):
    result = await process_request(response, coroutine=task_status_app.get_task_status_by_tasks_run_id(tasks_run_id))
    return result


@router_app.get(
    "/tasksRunning/condition/id/{tasks_running_id}", response_model=TasksRunningStatusLoadedResponse,
    description="根据id获取正在运行的任务状态", name="根据id获取正在运行的任务状态"
)
async def get_tasks_running_status_by_running_id(
        response: Response,
        tasks_running_id: str = Path(..., description="tasks running id", example="xxx")
):
    result = await process_request(response, coroutine=task_running_app.get_tasks_running_by_id(tasks_running_id))
    return result


@router_app.get(
    "/tasksRun/reference/tasksRunning/{tasks_running_id}", response_model=TasksRunningMappingResponse,
    name="根据tasks running id 获取对应 tasks run id", description="根据tasks running id 获取对应 tasks run id"
)
async def get_tasks_run_id_by_tasks_running_id(
        response: Response,
        tasks_running_id: str = Path(..., description="tasks running id", example="xxx")
):
    result = await process_request(
        response, coroutine=task_running_app.get_tasks_run_id_by_tasks_running_id(tasks_running_id)
    )
    return result
