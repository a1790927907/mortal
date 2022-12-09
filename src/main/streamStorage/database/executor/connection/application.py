from src.main.utils.logger import logger
from sqlalchemy.dialects.postgresql.dml import Insert
from src.main.streamStorage.database.executor.connection.model import Connection
from src.main.streamStorage.database.tables.connection import table as connection_table
from src.main.streamStorage.database.base.application import Application as BaseApplication


class Application(BaseApplication):
    table = connection_table

    async def upsert_connection(self, connection: Connection):
        insert_sql: Insert = Insert(self.table, inline=True).values(connection.dict())
        insert_sql = insert_sql.on_conflict_do_update(
            index_elements=["id"], set_=connection.dict()
        )
        db = await self.get_db()
        await db.execute(insert_sql)
        logger.info("存储 connection: {} 成功, reference: {}".format(connection.id, connection.referenceId))

    async def get_connection_by_id(self, connection_id: str):
        query = self.table.select().filter_by(id=connection_id)
        result = await self.fetch_one(query)
        return result

    async def get_connection_by_reference_id(self, reference_id: int):
        query = self.table.select().filter_by(referenceId=reference_id)
        result = await self.fetch_one(query)
        return result

    async def get_connections(self, *, limit: int = 0, offset: int = 0):
        query = self.table.select()
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        query = query.order_by(self.table.c.updateTime.desc())
        result = await self.fetch_all(query)
        return result
