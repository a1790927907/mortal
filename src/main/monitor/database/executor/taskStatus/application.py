from src.main.utils.logger import logger
from sqlalchemy.dialects.postgresql.dml import Insert
from src.main.monitor.database.executor.taskStatus.model import TaskStatus
from src.main.monitor.database.tables.taskStatus import table as task_status_table
from src.main.monitor.database.executor.base.application import Application as BaseApplication


class Application(BaseApplication):
    table = task_status_table

    async def upsert_task_status(self, request_info: TaskStatus):
        insert_sql: Insert = Insert(inline=True, table=self.table).values(request_info.dict())
        insert_sql = insert_sql.on_conflict_do_update(
            index_elements=["id"], set_=request_info.dict()
        )
        db = await self.get_db()
        await db.execute(insert_sql)
        logger.info("存储 status {}, task {}, run id {} 成功".format(
            request_info.id, request_info.taskId, request_info.runId
        ))

    async def get_status_by_run_id(self, run_id: str):
        query = self.table.select().filter_by(runId=run_id)
        result = await self.fetch_all(query)
        return result

    async def get_status_by_id(self, status_id: str):
        query = self.table.select().filter_by(id=status_id)
        result = await self.fetch_one(query)
        return result
