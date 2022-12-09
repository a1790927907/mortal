from typing import Type
from src.main.streamStorage.config import Settings
from src.main.streamStorage.backend.task.application import Application as TaskApplication
from src.main.streamStorage.backend.connection.application import Application as ConnectionApplication


class Application:
    def __init__(self, settings: Type[Settings]):
        self.settings = settings
        self.task_app = TaskApplication(self.settings)
        self.connection_app = ConnectionApplication(self.settings)


application = Application(Settings)
