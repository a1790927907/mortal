from src.main.streamController.exception import StreamControllerException
from src.main.streamController.external.application import application as external_app
from src.main.streamController.operator.loader.base.application import Application as BaseApplication


class Application(BaseApplication):
    async def get_tasks_by_connection_id(self, connection_id: str):
        connection = await external_app.storage_app.get_connection_by_connection_id(connection_id)
        if connection is None:
            raise StreamControllerException("connection id {} 不存在".format(connection_id), error_code=404)
        tasks = await external_app.storage_app.get_tasks_by_connection(connection_id)
        grouped_tasks = self.rank_tasks(connection["payload"], tasks)
        return {"result": {"tasks": grouped_tasks, "connection": connection}}
