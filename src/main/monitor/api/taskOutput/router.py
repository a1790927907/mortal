from src.main.monitor.config import Settings
from fastapi import Response, APIRouter, Path
from src.main.monitor.api.base.app import process_request
from src.main.monitor.operator.taskOutput.model import SaveTaskOutputRequestInfo
from src.main.monitor.api.taskOutput.model import SaveTaskOutputResponse, TaskOutputResponse
from src.main.monitor.operator.taskOutput.application import Application as TasksOutputApplication


router_app = APIRouter(prefix="/monitor/taskOutput", tags=["taskOutput"])
app = TasksOutputApplication(Settings)


@router_app.post(
    "/store/save", response_model=SaveTaskOutputResponse, name="创建一个task output记录",
    description="创建一个task output记录"
)
async def save_task_output(response: Response, request_info: SaveTaskOutputRequestInfo):
    result = await process_request(response, coroutine=app.save_task_output(request_info))
    return result


@router_app.get(
    "/condition/status/{task_status_id}", response_model=TaskOutputResponse,
    name="根据 status id 获取一个 task output 记录", description="根据 status id 获取一个 task output 记录"
)
async def get_task_output_by_task_status_id(
        response: Response,
        task_status_id: str = Path(..., description="task status id", example="xxx")
):
    result = await process_request(response, coroutine=app.get_task_output_by_status_id(task_status_id))
    return result
