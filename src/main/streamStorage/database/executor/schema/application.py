from src.main.utils.logger import logger
from sqlalchemy.dialects.postgresql.dml import Insert
from src.main.streamStorage.database.executor.schema.model import InputSchema
from src.main.streamStorage.database.tables.schema import table as schema_table
from src.main.streamStorage.database.base.application import Application as BaseApplication


class Application(BaseApplication):
    table = schema_table

    async def upsert_schema(self, request_info: InputSchema):
        insert_sql: Insert = Insert(self.table, inline=True).values(request_info.dict())
        insert_sql = insert_sql.on_conflict_do_update(
            index_elements=["id"],
            set_=request_info.dict()
        )
        db = await self.get_db()
        await db.execute(insert_sql)
        logger.info("存储 schema {} 成功".format(request_info.id))

    async def get_schema_by_id(self, schema_id: str):
        query = self.table.select().filter_by(id=schema_id)
        result = await self.fetch_one(query)
        return result

    async def get_schema_by_connection_id(self, connection_id: str):
        query = self.table.select().filter_by(connectionId=connection_id)
        result = await self.fetch_one(query)
        return result
