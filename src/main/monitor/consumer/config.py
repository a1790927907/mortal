import os
import aiohttp
import asyncio

from src.main.utils.custom_aiohttp_session import HoMuraSession


class Settings:
    kafka_server: str = os.getenv("KAFKA_SERVER", "localhost:9092")
    kafka_monitor_tasks_run_worker_topic: str = os.getenv(
        "KAFKA_MONITOR_TASKS_RUN_WORKER_TOPIC", "stream-monitor-tasks-run-worker"
    )
    kafka_monitor_tasks_run_worker_group_id: str = os.getenv(
        "KAFKA_MONITOR_TASKS_RUN_WORKER_GROUP_ID", "stream-monitor-tasks-run-worker-group"
    )
    kafka_monitor_tasks_run_worker_max_sem: int = int(os.getenv("KAFKA_MONITOR_TASKS_RUN_WORKER_MAX_SEM", "10"))

    kafka_monitor_task_status_worker_topic: str = os.getenv(
        "KAFKA_MONITOR_TASK_STATUS_WORKER_TOPIC", "stream-monitor-task-status-worker"
    )
    kafka_monitor_task_status_worker_group_id: str = os.getenv(
        "KAFKA_MONITOR_TASK_STATUS_WORKER_GROUP_ID", "stream-monitor-task-status-worker-group"
    )
    kafka_monitor_task_status_worker_max_sem: int = int(os.getenv("KAFKA_MONITOR_TASK_STATUS_WORKER_MAX_SEM", "10"))

    kafka_monitor_tasks_running_worker_topic: str = os.getenv(
        "KAFKA_MONITOR_TASKS_RUNNING_WORKER_TOPIC", "stream-monitor-tasks-running-worker"
    )
    kafka_monitor_tasks_running_worker_group_id: str = os.getenv(
        "KAFKA_MONITOR_TASKS_RUNNING_WORKER_GROUP_ID", "stream-monitor-tasks-running-worker-group"
    )
    kafka_monitor_tasks_running_worker_max_sem: int = int(os.getenv("KAFKA_MONITOR_TASKS_RUNNING_WORKER_MAX_SEM", "100"))

    monitor_server: str = os.getenv("MONITOR_SERVER", "http://localhost:13000")
    save_tasks_run_url: str = monitor_server + "/monitor/tasksRun/store/save/{tasks_run_id}"
    save_task_status_url: str = monitor_server + "/monitor/taskStatus/store/save"
    save_task_output_url: str = monitor_server + "/monitor/taskOutput/store/save"
    save_tasks_run_input_url: str = monitor_server + "/monitor/tasksRunInput/store/save"
    save_tasks_running_url: str = monitor_server + "/monitor/tasksRunning/store/{tasks_running_id}/save"
    delete_tasks_running_url: str = monitor_server + "/monitor/tasksRunning/condition/id/{tasks_running_id}"
    session: HoMuraSession = HoMuraSession(
        aiohttp.ClientSession, retry_interval=1, retry_when=lambda x: not isinstance(x, asyncio.TimeoutError)
    )
