from src.main.utils.logger import logger
from sqlalchemy.dialects.postgresql.dml import Insert
from src.main.monitor.database.executor.tasksRunning.model import TasksRunning
from src.main.monitor.database.tables.tasksRunning import table as tasks_running_table
from src.main.monitor.database.executor.base.application import Application as BaseApplication


class Application(BaseApplication):
    table = tasks_running_table

    async def upsert_tasks_running(self, request_info: TasksRunning):
        insert_sql: Insert = Insert(table=self.table, inline=True).values(request_info.dict())
        insert_sql = insert_sql.on_conflict_do_update(
            index_elements=["id"], set_=request_info.dict()
        )
        db = await self.get_db()
        await db.execute(insert_sql)
        logger.info("存储 tasks running {} 成功".format(request_info.id))

    async def get_tasks_running_by_connection_id(self, connection_id: str):
        query = self.table.select().filter_by(connectionId=connection_id)
        result = await self.fetch_all(query)
        return result

    async def get_tasks_running_by_id(self, tasks_running_id: str):
        query = self.table.select().filter_by(id=tasks_running_id)
        result = await self.fetch_one(query)
        return result

    async def delete_tasks_running_by_id(self, tasks_running_id: str):
        query = self.table.delete().filter_by(id=tasks_running_id)
        db = await self.get_db()
        await db.execute(query)
        logger.info("成功删除 tasks running {}".format(tasks_running_id))
