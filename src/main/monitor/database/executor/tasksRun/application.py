from src.main.utils.logger import logger
from sqlalchemy.dialects.postgresql.dml import Insert
from src.main.monitor.database.executor.tasksRun.model import TasksRun
from src.main.monitor.database.tables.tasksRun import table as tasks_run_table
from src.main.monitor.database.executor.base.application import Application as BaseApplication
from src.main.monitor.database.executor.tasksRun.model import SearchTasksRunRequestInfo, FilterInfo


class Application(BaseApplication):
    table = tasks_run_table

    async def create_tasks_run(self, request_info: TasksRun):
        insert_sql: Insert = Insert(table=self.table, inline=True).values(request_info.dict())
        db = await self.get_db()
        await db.execute(insert_sql)
        logger.info("存储 tasks run {} openid {} connection id {} 成功".format(
            request_info.id, request_info.openid, request_info.connectionId
        ))

    async def get_tasks_runs_by_connection_id(self, connection_id: str):
        query = self.table.select().filter_by(connectionId=connection_id).order_by(self.table.c.updateTime.desc())
        result = await self.fetch_all(query)
        return result

    async def get_tasks_runs_by_openid(self, openid: str):
        query = self.table.select().filter_by(openid=openid).order_by(self.table.c.updateTime.desc())
        result = await self.fetch_all(query)
        return result

    async def get_tasks_run_by_id(self, tasks_run_id: str):
        query = self.table.select().filter_by(id=tasks_run_id)
        result = await self.fetch_one(query)
        return result

    def process_filter_info(self, filter_info: FilterInfo):
        filter_info_source_mapping = {
            "updateTime": self.table.c.updateTime,
            "openid": self.table.c.openid,
            "status": self.table.c.status
        }
        source = filter_info_source_mapping[filter_info.by]
        if filter_info.factor == "eq":
            return source == filter_info.value
        elif filter_info.factor == "lte":
            return source <= filter_info.value
        elif filter_info.factor == "lt":
            return source < filter_info.value
        elif filter_info.factor == "gt":
            return source > filter_info.value
        else:
            return source >= filter_info.value

    def generate_search_query(self, request_info: SearchTasksRunRequestInfo):
        query = self.table.select().filter_by(connectionId=request_info.connectionId)
        criteria = []
        if request_info.filterInfo is not None:
            for filter_info in request_info.filterInfo:
                criteria.append(self.process_filter_info(filter_info))
        query = query.filter(*criteria)
        if request_info.order.by == "updateTime":
            if request_info.order.type == "desc":
                query = query.order_by(self.table.c.updateTime.desc())
            else:
                query = query.order_by(self.table.c.updateTime.asc())
        return query

    async def get_tasks_runs_number_after_search(self, request_info: SearchTasksRunRequestInfo) -> int:
        query = self.generate_search_query(request_info)
        result = await self.fetch_all(query)
        return len(result)

    async def search_tasks_run_by_request_info(self, request_info: SearchTasksRunRequestInfo):
        query = self.generate_search_query(request_info)
        query = query.limit(request_info.pageInfo.limit).offset(request_info.pageInfo.offset)
        result = await self.fetch_all(query)
        return result
