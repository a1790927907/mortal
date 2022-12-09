import asyncio
import selectors

from src.main.monitor.consumer.config import Settings
from src.main.monitor.consumer.worker.taskStatus.application import Application as TaskStatusApplication


if __name__ == '__main__':
    selector = selectors.SelectSelector()
    loop = asyncio.SelectorEventLoop(selector)
    asyncio.set_event_loop(loop)
    app = TaskStatusApplication(Settings)
    loop.run_until_complete(app.consume())
