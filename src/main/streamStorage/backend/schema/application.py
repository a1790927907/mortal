import os
import asyncio

from typing import Optional
from src.main.utils.model_generator import generate_model
from src.main.streamStorage.exception import StreamStorageException
from src.main.streamStorage.database.executor.schema.model import InputSchema
from src.main.streamStorage.backend.schema.model import SaveSchemaRequestInfo
from src.main.client.redis.application import application as redis_application
from src.main.utils.data_process_utils import format_dict_to_be_json_serializable
from src.main.streamStorage.base.application import Application as BaseApplication
from src.main.streamStorage.database.executor.application import application as database_application


class Application(BaseApplication):
    @staticmethod
    async def upsert_schema(request_info: InputSchema):
        await database_application.schema_app.upsert_schema(request_info)
        return {"id": request_info.id, "connectionId": request_info.connectionId}

    async def create_schema(self, request_info: SaveSchemaRequestInfo):
        request_info = InputSchema(**request_info.dict())
        result = await self.upsert_schema(request_info)
        return result

    async def update_schema(self, request_info: SaveSchemaRequestInfo, schema_id: str):
        schema = await database_application.schema_app.get_schema_by_id(schema_id)
        if schema is None:
            raise StreamStorageException("schema {} 不存在".format(schema_id), error_code=404)
        params = request_info.dict()
        params["id"] = schema_id
        request_info = InputSchema(**params)
        result = await self.upsert_schema(request_info)
        return result

    @staticmethod
    async def _get_schema_by_connection_id(connection_id: str):
        result = await database_application.schema_app.get_schema_by_connection_id(connection_id)
        return result

    async def validate_schema(self, request_info: SaveSchemaRequestInfo, schema_id: Optional[str]):
        schema = await self._get_schema_by_connection_id(request_info.connectionId)
        if schema is not None and schema_id is not None:
            if schema["id"] != schema_id:
                raise StreamStorageException("connection id: {} 已存在, 对应的schema id为 {}, 无法更新".format(
                    request_info.connectionId, schema["id"]
                ), error_code=400)
        elif schema is not None and schema_id is None:
            raise StreamStorageException("connection id: {} 已存在, 对应的schema id为 {}, 无法创建".format(
                request_info.connectionId, schema["id"]
            ), error_code=400)

    @staticmethod
    async def _generate_schema_model(schema: dict, schema_id: str):
        file_name = "{}.py".format(schema_id)
        path = os.path.join(redis_application.settings.model_cache_dir, file_name)
        loop = asyncio.get_running_loop()
        output_path = await loop.run_in_executor(None, generate_model, schema, path)
        await redis_application.set_schema_model_cache(schema_id, {"path": output_path, "filename": file_name})

    async def _save_schema(self, request_info: SaveSchemaRequestInfo, *, schema_id: Optional[str] = None):
        await self.validate_schema(request_info, schema_id)
        if schema_id is None:
            result = await self.create_schema(request_info)
        else:
            result = await self.update_schema(request_info, schema_id)
        await self._generate_schema_model(request_info.info, result["id"])
        return result

    async def save_schema(self, request_info: SaveSchemaRequestInfo, *, schema_id: Optional[str] = None):
        result = await self._save_schema(request_info, schema_id=schema_id)
        return {"result": result}

    @staticmethod
    async def get_schema_by_id(schema_id: str):
        # TODO: 带上 model path
        result = await database_application.schema_app.get_schema_by_id(schema_id)
        if result is None:
            raise StreamStorageException("schema {} 不存在".format(schema_id), error_code=404)
        format_dict_to_be_json_serializable(result)
        return {"result": result}

    async def get_schema_by_connection_id(self, connection_id: str):
        result = await self._get_schema_by_connection_id(connection_id)
        if result is None:
            raise StreamStorageException("connection {} 对应schema不存在".format(connection_id), error_code=404)
        format_dict_to_be_json_serializable(result)
        return {"result": result}
