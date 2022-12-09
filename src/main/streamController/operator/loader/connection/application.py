import asyncio

from src.main.streamController.external.application import application as external_app
from src.main.streamController.operator.loader.base.application import Application as BaseApplication


class Application(BaseApplication):
    @staticmethod
    async def get_schema_by_connection_id(connection_id: str):
        schema = await external_app.storage_app.get_schema_by_connection_id(connection_id)
        return schema

    async def _get_connections(self):
        connections = await external_app.storage_app.get_connection_by_connection_id("all")
        schema_result = await asyncio.gather(*[
            self.get_schema_by_connection_id(connection["id"])
            for connection in connections
        ])
        result = [
            {"connection": conn, "schemaInfo": schema, "active": schema is not None}
            for conn, schema in zip(connections, schema_result)
        ]
        return result

    async def get_connections(self):
        result = await self._get_connections()
        return {"result": result}

    async def _get_connection_by_reference_id(self, reference_id: int):
        connection = await external_app.storage_app.get_connection_by_reference_id(reference_id)
        schema = await self.get_schema_by_connection_id(connection["id"])
        return {"connection": connection, "schemaInfo": schema, "active": schema is not None}

    async def get_connection_by_reference_id(self, reference_id: int):
        result = await self._get_connection_by_reference_id(reference_id)
        return {"result": result}
