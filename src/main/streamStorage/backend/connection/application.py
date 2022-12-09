from typing import Optional, Union
from src.main.streamStorage.exception import StreamStorageException
from src.main.streamStorage.base.application import Application as BaseApplication
from src.main.streamStorage.database.executor.application import application as database_app
from src.main.streamStorage.database.executor.connection.model import Connection as DatabaseConnection
from src.main.utils.data_process_utils import format_list_to_be_json_serializable, format_dict_to_be_json_serializable
from src.main.streamStorage.backend.connection.model import GetAllConnectionsRequestInfo, \
    CreateConnectionRequestInfo, UpdateConnectionRequestInfo


class Application(BaseApplication):
    @staticmethod
    async def upsert_connection(request_info: DatabaseConnection):
        await database_app.connection_app.upsert_connection(request_info)
        return {"id": request_info.id, "payload": request_info.dict()["payload"]}

    async def create_connection(self, request_info: CreateConnectionRequestInfo):
        request_info = DatabaseConnection(**request_info.dict())
        result = await self.upsert_connection(request_info)
        return result

    @staticmethod
    async def _get_connection_by_id(connection_id: str):
        result = await database_app.connection_app.get_connection_by_id(connection_id)
        if result is None:
            raise StreamStorageException("connection {} 不存在".format(connection_id), error_code=404)
        return result

    async def get_connection_by_id(self, connection_id: str):
        result = await self._get_connection_by_id(connection_id)
        format_dict_to_be_json_serializable(result)
        return {"result": result}

    @staticmethod
    async def _get_connection_by_reference_id(reference_id: int):
        result = await database_app.connection_app.get_connection_by_reference_id(reference_id)
        if result is None:
            raise StreamStorageException("connection reference id: {} 不存在".format(reference_id), error_code=404)
        return result

    async def get_connection_by_reference_id(self, reference_id: int):
        result = await self._get_connection_by_reference_id(reference_id)
        format_dict_to_be_json_serializable(result)
        return {"result": result}

    async def update_connection(self, request_info: UpdateConnectionRequestInfo, connection_id: str):
        connection = await self._get_connection_by_id(connection_id)
        request_info = {key: value for key, value in request_info.dict().items() if value is not None}
        request_info = {**connection, **request_info}
        request_info.pop("updateTime", None)
        request_info = DatabaseConnection(**request_info)
        result = await self.upsert_connection(request_info)
        return result

    async def _save_connection(
            self, request_info: Union[CreateConnectionRequestInfo, UpdateConnectionRequestInfo], *,
            connection_id: Optional[str] = None
    ):
        if connection_id is None:
            result = await self.create_connection(request_info)
        else:
            result = await self.update_connection(request_info, connection_id)
        return {"result": result}

    async def save_connection(
            self, request_info: Union[CreateConnectionRequestInfo, UpdateConnectionRequestInfo], *,
            connection_id: Optional[str] = None
    ):
        result = await self._save_connection(request_info, connection_id=connection_id)
        return result

    @staticmethod
    async def get_connections(request_info: GetAllConnectionsRequestInfo):
        result = await database_app.connection_app.get_connections(limit=request_info.limit, offset=request_info.offset)
        format_list_to_be_json_serializable(result)
        return {"result": result}
