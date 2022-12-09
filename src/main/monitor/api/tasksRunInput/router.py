from src.main.monitor.config import Settings
from fastapi import APIRouter, Response, Path
from src.main.monitor.api.base.app import process_request
from src.main.monitor.operator.tasksRunInput.model import SaveTasksRunInputRequestInfo
from src.main.monitor.api.tasksRunInput.model import SaveTasksRunInputResponse, TasksRunInputResponse
from src.main.monitor.operator.tasksRunInput.application import Application as TasksRunInputApplication


router_app = APIRouter(prefix="/monitor/tasksRunInput", tags=["tasksRunInput"])
app = TasksRunInputApplication(Settings)


@router_app.put(
    "/store/save", response_model=SaveTasksRunInputResponse, name="存储一个tasks run的input",
    description="存储一个tasks run的input"
)
async def save_tasks_run_input(response: Response, request_info: SaveTasksRunInputRequestInfo):
    result = await process_request(response, coroutine=app.save_tasks_run_input(request_info))
    return result


@router_app.get(
    "/reference/tasksRun/{tasks_run_id}", response_model=TasksRunInputResponse, name="根据tasks run id获取其input",
    description="根据tasks run id获取其input"
)
async def get_tasks_run_input_by_run_id(
        response: Response, tasks_run_id: str = Path(..., description="tasks run id", example="xxx")
):
    result = await process_request(response, coroutine=app.get_tasks_input_by_run_id(tasks_run_id))
    return result
