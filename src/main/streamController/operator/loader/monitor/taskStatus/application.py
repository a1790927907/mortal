from src.main.streamController.exception import StreamControllerException
from src.main.streamController.external.application import application as external_app
from src.main.streamController.operator.loader.monitor.base.application import Application as BaseApplication


class Application(BaseApplication):
    @staticmethod
    async def _fetch_tasks_run_by_id(tasks_run_id: str):
        tasks_run_instance = await external_app.monitor_app.get_tasks_run_by_run_id(tasks_run_id)
        if tasks_run_instance is None:
            raise StreamControllerException("tasks run id: {} 不存在".format(tasks_run_id), error_code=404)
        return tasks_run_instance

    async def get_task_status_by_tasks_run_id(self, tasks_run_id: str):
        tasks_run_instance = await self._fetch_tasks_run_by_id(tasks_run_id)
        all_task_status = await external_app.monitor_app.get_task_status_by_tasks_run_id(tasks_run_id)
        result = await self.generate_task_status_result(
            all_task_status, tasks_run_instance["connectionId"], run_id=tasks_run_id
        )
        return {"result": result}
