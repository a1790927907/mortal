from typing import Type
from src.main.streamController.config import Settings
from src.main.streamController.external.n8n.application import Application as N8NApplication
from src.main.streamController.external.monitor.application import Application as MonitorApplication
from src.main.streamController.external.streamParser.application import Application as ParserApplication
from src.main.streamController.external.streamStorage.application import Application as StorageApplication
from src.main.streamController.external.streamActuator.application import Application as ActuatorApplication


class Application:
    def __init__(self, settings: Type[Settings]):
        self.settings = settings
        self.parser_app = ParserApplication(self.settings)
        self.actuator_app = ActuatorApplication(self.settings)
        self.n8n_app = N8NApplication(self.settings)
        self.storage_app = StorageApplication(self.settings)
        self.monitor_app = MonitorApplication(self.settings)


application = Application(Settings)
