from typing import Union
from fastapi import APIRouter, Response, Path, Query, Depends
from src.main.streamStorage.api.base.app import process_request
from src.main.streamStorage.backend.application import application as backend_app
from src.main.streamStorage.api.connection.model import GetAllConnectionsResponse, UpsertConnectionResponse, \
    GetConnectionResponse
from src.main.streamStorage.backend.connection.model import CreateConnectionRequestInfo, UpdateConnectionRequestInfo, \
    GetAllConnectionsRequestInfo


router_app = APIRouter(prefix="/connection", tags=["connection"])
app = backend_app.connection_app


@router_app.put(
    "/store/save", response_model=UpsertConnectionResponse, name="保存一个connection", description="保存一个connection"
)
async def save_connection(
        response: Response, request_info: Union[CreateConnectionRequestInfo, UpdateConnectionRequestInfo],
        connection_id: str = Query(default=None, description="connection 不填写默认创建", example="xxx")
):
    result = await process_request(response, app.save_connection(request_info, connection_id=connection_id))
    return result


@router_app.get(
    "/all", response_model=GetAllConnectionsResponse, name="获取所有connection", description="获取所有connection"
)
async def get_connections(
        response: Response, request_info: GetAllConnectionsRequestInfo = Depends(GetAllConnectionsRequestInfo)
):
    result = await process_request(response, app.get_connections(request_info))
    return result


@router_app.get(
    "/{connection_id}", response_model=GetConnectionResponse, name="获取单个connection",
    description="获取单个connection"
)
async def get_connection_by_id(
        response: Response, connection_id: str = Path(..., description="connection id", example="xxx")
):
    result = await process_request(response, app.get_connection_by_id(connection_id))
    return result


@router_app.get(
    "/reference/{reference_id}", response_model=GetConnectionResponse, name="根据外键获取单个connection",
    description="根据外键获取单个connection"
)
async def get_connection_by_reference_id(
        response: Response, reference_id: int = Path(..., description="reference id", example="xxx")
):
    result = await process_request(response, app.get_connection_by_reference_id(reference_id))
    return result
