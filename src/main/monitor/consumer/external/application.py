from typing import Type
from src.main.monitor.consumer.config import Settings
from src.main.monitor.consumer.external.tasksRun.application import Application as TasksRunApplication
from src.main.monitor.consumer.external.taskStatus.application import Application as TaskStatusApplication
from src.main.monitor.consumer.external.taskOutput.application import Application as TaskOutputApplication
from src.main.monitor.consumer.external.tasksRunning.application import Application as TasksRunningApplication
from src.main.monitor.consumer.external.tasksRunInput.application import Application as TasksRunInputApplication


class Application:
    def __init__(self, settings: Type[Settings]):
        self.settings = settings
        self.tasks_run_app = TasksRunApplication(self.settings)
        self.tasks_running_app = TasksRunningApplication(self.settings)
        self.task_status_app = TaskStatusApplication(self.settings)
        self.task_output_app = TaskOutputApplication(self.settings)
        self.tasks_run_input_app = TasksRunInputApplication(self.settings)


application = Application(Settings)
