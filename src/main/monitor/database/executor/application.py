import databases

from typing import Type
from src.main.monitor.config import Settings
from src.main.monitor.base.application import Application as BaseApplication
from src.main.monitor.database.executor.tasksRun.application import Application as TasksRunApplication
from src.main.monitor.database.executor.taskStatus.application import Application as TaskStatusApplication
from src.main.monitor.database.executor.taskOutput.application import Application as TasksOutputApplication
from src.main.monitor.database.executor.tasksRunning.application import Application as TasksRunningApplication
from src.main.monitor.database.executor.tasksRunInput.application import Application as TasksRunInputApplication


class Application(BaseApplication):
    def __init__(self, settings: Type[Settings]):
        super().__init__(settings)
        self.db = databases.Database(self.settings.db_url)
        self.tasks_run_app = TasksRunApplication(self.settings, self.db)
        self.tasks_running_app = TasksRunningApplication(self.settings, self.db)
        self.tasks_run_input_app = TasksRunInputApplication(self.settings, self.db)
        self.task_status_app = TaskStatusApplication(self.settings, self.db)
        self.task_output_app = TasksOutputApplication(self.settings, self.db)

    async def init_connection(self):
        await self.db.connect()


application = Application(Settings)
