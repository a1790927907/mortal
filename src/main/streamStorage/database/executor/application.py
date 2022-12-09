from typing import Type
from src.main.streamStorage.config import Settings
from src.main.streamStorage.database.base.application import Base
from src.main.streamStorage.database.executor.task.application import Application as TaskApplication
from src.main.streamStorage.database.executor.schema.application import Application as SchemaApplication
from src.main.streamStorage.database.executor.connection.application import Application as ConnectionApplication


class Application:
    def __init__(self, settings: Type[Settings]):
        self.settings = settings
        self.task_app = TaskApplication(self.settings)
        self.connection_app = ConnectionApplication(self.settings)
        self.schema_app = SchemaApplication(self.settings)

    @staticmethod
    def init_tables():
        Base.metadata.create_all()


application = Application(Settings)
