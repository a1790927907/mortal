from src.main.monitor.config import Settings
from fastapi import APIRouter, Response, Path
from src.main.monitor.api.base.app import process_request
from src.main.monitor.operator.tasksRunning.model import SaveTasksRunningRequestInfo
from src.main.monitor.operator.tasksRunning.application import Application as TasksRunningApplication
from src.main.monitor.api.tasksRunning.model import SaveTasksRunningResponse, TasksRunningResponse, \
    MultipleTasksRunningResponse, DeleteTasksRunningResponse


router_app = APIRouter(prefix="/monitor/tasksRunning", tags=["tasksRunning"])
app = TasksRunningApplication(Settings)


@router_app.put(
    "/store/{tasks_running_id}/save", response_model=SaveTasksRunningResponse, name="存储一个tasks running",
    description="存储一个tasks running"
)
async def save_tasks_running(
        response: Response, request_info: SaveTasksRunningRequestInfo,
        tasks_running_id: str = Path(..., description="tasks running id", example="xxx")
):
    result = await process_request(
        response, coroutine=app.save_tasks_running(request_info, tasks_running_id=tasks_running_id)
    )
    return result


@router_app.get(
    "/reference/connection/{connection_id}", response_model=MultipleTasksRunningResponse,
    name="根据connection id获取其正在运行的任务", description="根据connection id获取其正在运行的任务"
)
async def get_tasks_running_by_connection_id(
        response: Response, connection_id: str = Path(..., description="connection id", example="xxx")
):
    result = await process_request(response, coroutine=app.get_tasks_running_by_connection_id(connection_id))
    return result


@router_app.get(
    "/condition/id/{tasks_running_id}", response_model=TasksRunningResponse, name="根据id获取正在运行的任务实体",
    description="根据id获取正在运行的任务实体"
)
async def get_tasks_running_by_id(
        response: Response, tasks_running_id: str = Path(..., description="tasks running id", example="xxx")
):
    result = await process_request(response, coroutine=app.get_tasks_running_by_id(tasks_running_id))
    return result


@router_app.delete(
    "/condition/id/{tasks_running_id}", response_model=DeleteTasksRunningResponse, name="根据id删除正在运行的任务实体",
    description="根据id删除正在运行的任务实体"
)
async def delete_tasks_running_by_id(
        response: Response, tasks_running_id: str = Path(..., description="tasks running id", example="xxx")
):
    result = await process_request(response, coroutine=app.delete_tasks_running_by_id(tasks_running_id))
    return result
