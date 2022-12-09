from typing import Union
from fastapi import APIRouter, Response, Path, Query
from src.main.streamStorage.api.base.app import process_request
from src.main.streamStorage.backend.application import application as backend_app
from src.main.streamStorage.backend.task.model import CreateTaskRequestInfo, UpdateTaskRequestInfo
from src.main.streamStorage.api.task.model import UpsertTaskResponse, GetTaskResponse, GetTasksResponse


router_app = APIRouter(prefix="/task", tags=["task"])
app = backend_app.task_app


@router_app.put("/store/save", response_model=UpsertTaskResponse, description="保存一个task", name="保存一个task")
async def save_task(
        response: Response, request_info: Union[CreateTaskRequestInfo, UpdateTaskRequestInfo],
        task_id: str = Query(default=None, description="task id 不传即为创建", example="xxx")
):
    result = await process_request(response, app.save_task(request_info, task_id=task_id))
    return result


@router_app.put("/save/{task_id}", response_model=UpsertTaskResponse, description="保存一个task", name="保存一个task")
async def save_task_by_id(
        response: Response, request_info: CreateTaskRequestInfo,
        task_id: str = Path(..., description="task id", example="xxx")
):
    result = await process_request(response, app.save_task_by_id(request_info, task_id))
    return result


@router_app.get("/{task_id}", response_model=GetTaskResponse, description="根据id获取一个task", name="根据id获取一个task")
async def get_task_by_id(response: Response, task_id: str = Path(..., description="task id", example="xxx")):
    result = await process_request(response, app.get_task_by_id(task_id=task_id))
    return result


@router_app.get(
        "/reference/connection/{connection_id}", response_model=GetTasksResponse,
        description="根据 connection id 获取相关task", name="根据 connection id 获取相关task"
)
async def get_tasks_by_connection_id(
        response: Response, connection_id: str = Path(..., description="connection id", example="xx")
):
    result = await process_request(response, app.get_tasks_by_connection_id(connection_id))
    return result
