from src.main.streamStorage.config import Settings
from fastapi import APIRouter, Response, Query, Path
from src.main.streamStorage.api.base.app import process_request
from src.main.streamStorage.backend.schema.model import SaveSchemaRequestInfo
from src.main.streamStorage.api.schema.model import SaveSchemaResponse, GetSchemaResponse
from src.main.streamStorage.backend.schema.application import Application as SchemaApplication

router_app = APIRouter(prefix="/schema", tags=["schema"])
app = SchemaApplication(Settings)


@router_app.put(
    "/store/save", response_model=SaveSchemaResponse, name="存储一个schema", description="存储一个schema"
)
async def save_schema(
        response: Response, request_info: SaveSchemaRequestInfo,
        schema_id: str = Query(default=None, description="schema id 不填写则为创建", example="xxx")
):
    result = await process_request(response, coroutine=app.save_schema(request_info, schema_id=schema_id))
    return result


@router_app.get(
    "/reference/connection/{connection_id}", response_model=GetSchemaResponse, name="根据connection获取一个schema",
    description="根据connection获取一个schema"
)
async def get_schema_by_connection_id(
        response: Response, connection_id: str = Path(..., description="connection id", example="xxx")
):
    result = await process_request(response, coroutine=app.get_schema_by_connection_id(connection_id))
    return result


@router_app.get(
    "/{schema_id}", response_model=GetSchemaResponse, name="根据schema id获取一个schema",
    description="根据schema id获取一个schema"
)
async def get_schema_by_id(
        response: Response, schema_id: str = Path(..., description="schema id", example="xxx")
):
    result = await process_request(response, coroutine=app.get_schema_by_id(schema_id))
    return result
