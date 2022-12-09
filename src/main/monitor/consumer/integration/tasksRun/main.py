import asyncio
import selectors

from src.main.monitor.consumer.config import Settings
from src.main.monitor.consumer.worker.tasksRun.application import Application as TasksRunApplication


if __name__ == '__main__':
    selector = selectors.SelectSelector()
    loop = asyncio.SelectorEventLoop(selector)
    asyncio.set_event_loop(loop)
    app = TasksRunApplication(Settings)
    loop.run_until_complete(app.consume())
