from src.main.utils.logger import logger
from sqlalchemy.dialects.postgresql.dml import Insert
from src.main.streamStorage.database.executor.task.model import Task
from src.main.streamStorage.database.tables.task import table as task_table
from src.main.streamStorage.database.base.application import Application as BaseApplication


class Application(BaseApplication):
    table = task_table

    async def upsert_task(self, task: Task):
        insert_sql: Insert = Insert(self.table, inline=True).values(task.dict())
        insert_sql = insert_sql.on_conflict_do_update(
            index_elements=["id"], set_=task.dict()
        )
        db = await self.get_db()
        await db.execute(insert_sql)
        logger.info("存储 task: id {}, name: {} 成功".format(task.id, task.name))

    async def get_task_by_id(self, task_id: str):
        query = self.table.select().filter_by(id=task_id)
        result = await self.fetch_one(query)
        return result

    async def get_tasks_by_connection_id(self, connection_id: str):
        query = self.table.select().filter_by(connectionId=connection_id).order_by(self.table.c.updateTime.desc())
        result = await self.fetch_all(query)
        return result

    async def delete_task_by_id(self, task_id: str):
        query = self.table.delete().filter_by(id=task_id)
        db = await self.get_db()
        await db.execute(query)
        logger.info("删除 task {} 成功".format(task_id))
