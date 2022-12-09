import asyncio
import selectors

from src.main.monitor.consumer.config import Settings
from src.main.monitor.consumer.worker.tasksRunning.application import Application


if __name__ == '__main__':
    app = Application(Settings)
    selector = selectors.SelectSelector()
    loop = asyncio.SelectorEventLoop(selector)
    asyncio.set_event_loop(loop)
    loop.run_until_complete(app.consume())
