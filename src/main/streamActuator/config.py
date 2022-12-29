import os
import asyncio
import aiohttp
from src.main.utils.custom_aiohttp_session import HoMuraSession
from src.main.globalSettings.config import Settings as globalSettings


tags_metadata = [
    {
        "name": "trigger",
        "description": "触发器相关"
    },
    {
        "name": "settings",
        "description": "配置相关"
    }
]


class Settings:
    author: str = "zyh"
    version: str = "1.0.0"
    description: str = "he"
    kafka_server: str = os.getenv("KAFKA_SERVER", "localhost:9092")
    kafka_monitor_tasks_run_worker_topic: str = os.getenv(
        "KAFKA_MONITOR_TASKS_RUN_WORKER_TOPIC", "stream-monitor-tasks-run-worker"
    )
    kafka_monitor_task_status_worker_topic: str = os.getenv(
        "KAFKA_MONITOR_TASK_STATUS_WORKER_TOPIC", "stream-monitor-task-status-worker"
    )
    kafka_monitor_tasks_running_worker_topic: str = os.getenv(
        "KAFKA_MONITOR_TASK_STATUS_WORKER_TOPIC", "stream-monitor-tasks-running-worker"
    )
    actuator_monitor_queue_size: int = int(os.getenv("ACTUATOR_MONITOR_QUEUE_SIZE", "3"))
    function_codes_dir: str = globalSettings.function_codes_dir
    session: HoMuraSession = HoMuraSession(
        aiohttp.ClientSession, retry_when=lambda x: not isinstance(x, asyncio.TimeoutError), retry_interval=1
    )

    @classmethod
    def to_dict(cls):
        result = {}
        for key, value in cls.__annotations__.items():
            val = getattr(cls, key, None)
            if isinstance(val, str) or isinstance(val, int) or isinstance(val, float):
                result[key] = val
        return result
