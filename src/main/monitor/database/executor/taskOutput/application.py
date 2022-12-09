from src.main.utils.logger import logger
from sqlalchemy.dialects.postgresql.dml import Insert
from src.main.monitor.database.executor.taskOutput.model import TaskOutput
from src.main.monitor.database.tables.taskOutput import table as task_output_table
from src.main.monitor.database.executor.base.application import Application as BaseApplication


class Application(BaseApplication):
    table = task_output_table

    async def save_task_output(self, request_info: TaskOutput):
        db = await self.get_db()
        insert_sql: Insert = Insert(table=self.table, inline=True).values(request_info.dict())
        await db.execute(insert_sql)
        logger.info("存储output成功, status id: {}, task id: {}".format(
            request_info.taskStatusId, request_info.taskId
        ))

    async def get_task_output_by_task_status_id(self, task_status_id: str):
        query = self.table.select().filter_by(taskStatusId=task_status_id)
        result = await self.fetch_one(query)
        return result
