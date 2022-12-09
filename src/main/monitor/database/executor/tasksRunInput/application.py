from src.main.utils.logger import logger
from sqlalchemy.dialects.postgresql.dml import Insert
from src.main.monitor.database.executor.tasksRunInput.model import TasksRunInput
from src.main.monitor.database.tables.tasksRunInput import table as tasks_run_input_table
from src.main.monitor.database.executor.base.application import Application as BaseApplication


class Application(BaseApplication):
    table = tasks_run_input_table

    async def save_tasks_run_input(self, request_info: TasksRunInput):
        insert_sql: Insert = Insert(table=self.table, inline=True).values(request_info.dict())
        insert_sql = insert_sql.on_conflict_do_update(
            index_elements=["runId"], set_=request_info.dict()
        )
        db = await self.get_db()
        await db.execute(insert_sql)
        logger.info("存储tasks run input成功, id: {} run id: {}".format(request_info.id, request_info.runId))

    async def get_tasks_run_input_by_run_id(self, run_id: str):
        query = self.table.select().filter_by(runId=run_id)
        result = await self.fetch_one(query)
        return result
