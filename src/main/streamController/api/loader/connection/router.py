from fastapi import APIRouter, Response, Path
from src.main.streamController.config import Settings
from src.main.streamController.api.base.app import process_request
from src.main.streamController.operator.loader.connection.application import Application
from src.main.streamController.api.loader.connection.model import ConnectionResponse, MultipleConnectionResponse


router_app = APIRouter(prefix="/stream/reference/connection", tags=["connections"])
app = Application(Settings)


@router_app.get(
    "/all", response_model=MultipleConnectionResponse, name="获取全部connection", description="获取全部connection"
)
async def get_connections(response: Response):
    result = await process_request(response, coroutine=app.get_connections())
    return result


@router_app.get(
    "/condition/{reference_id}", response_model=ConnectionResponse, name="根据reference id 获取 connection",
    description="根据reference id 获取 connection"
)
async def get_connection_by_reference_id(
    response: Response, reference_id: int = Path(..., description="connection binding reference id", example="xxx")
):
    result = await process_request(response, coroutine=app.get_connection_by_reference_id(reference_id))
    return result
