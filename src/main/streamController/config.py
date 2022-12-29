import os
import aiohttp
import asyncio

from src.main.utils.custom_aiohttp_session import HoMuraSession

tags_metadata = [
    {
        "name": "n8n",
        "description": "n8n相关"
    },
    {
        "name": "trigger",
        "description": "trigger相关"
    },
    {
        "name": "settings",
        "description": "配置相关"
    },
    {
        "name": "tasks",
        "description": "任务相关"
    },
    {
        "name": "monitor",
        "description": "监控相关"
    },
    {
        "name": "connections",
        "description": "工作流相关"
    }
]


class Settings:
    author: str = "zyh"
    version: str = "1.0.0"
    description: str = ""

    n8n_api_key: str = os.getenv("N8N_API_KEY", "n8n_api_bed6acfeb062aa080ea4741b78bb"
                                                "c3aee022d990bdd7479af71f8d09211d1f75b8cf0bed1c4b5044")
    n8n_api_server: str = os.getenv("N8N_API_SERVER", "http://localhost:5678")
    n8n_get_workflow_by_id_url: str = n8n_api_server + "/api/v1/workflows/{id}"
    stream_parser_server: str = os.getenv("STREAM_PARSER_SERVER", "http://localhost:16500")
    stream_parser_n8n_url: str = stream_parser_server + "/stream/n8n/parse"
    stream_actuator_server: str = os.getenv("STREAM_ACTUATOR_SERVER", "http://localhost:16000")
    trigger_stream_url: str = stream_actuator_server + "/stream/trigger/connection"
    stream_storage_server: str = os.getenv("STREAM_STORAGE_SERVER", "http://localhost:9400")
    save_stream_connection_url: str = stream_storage_server + "/connection/store/save"
    save_stream_task_url: str = stream_storage_server + "/task/save/{task_id}"
    get_stream_task_url: str = stream_storage_server + "/task/{task_id}"
    delete_stream_task_url: str = stream_storage_server + "/task/{task_id}"
    get_stream_connection_url: str = stream_storage_server + "/connection/{connection_id}"
    get_stream_connection_by_reference_url: str = stream_storage_server + "/connection/reference/{reference_id}"
    get_stream_tasks_by_connection_url: str = stream_storage_server + "/task/reference/connection/{connection_id}"
    get_stream_schema_by_connection_id_url: str = stream_storage_server + "/schema/reference/connection/{connection_id}"
    monitor_server: str = os.getenv("MONITOR_SERVER", "http://localhost:13000")
    get_tasks_run_by_connection_id_url: str = monitor_server + "/monitor/tasksRun/reference/connection/{connection_id}"
    get_tasks_run_by_id_url: str = monitor_server + "/monitor/tasksRun/condition/id/{tasks_run_id}"
    get_tasks_run_input_url: str = monitor_server + "/monitor/tasksRunInput/reference/tasksRun/{tasks_run_id}"
    get_all_task_status_by_tasks_run_id: str = monitor_server + "/monitor/taskStatus/reference/tasksRun/{run_id}"
    get_task_output_url: str = monitor_server + "/monitor/taskOutput/condition/status/{task_status_id}"
    get_tasks_running_by_id_url: str = monitor_server + "/monitor/tasksRunning/condition/id/{tasks_running_id}"
    get_tasks_runnings_by_connection_id_url: str = monitor_server + "/monitor/tasksRunning/" \
                                                                    "reference/connection/{connection_id}"
    session: HoMuraSession = HoMuraSession(
        aiohttp.ClientSession, retry_interval=1, retry_when=lambda x: not isinstance(x, asyncio.TimeoutError)
    )

    @classmethod
    def to_dict(cls):
        result = {}
        for key, value in cls.__annotations__.items():
            val = getattr(cls, key, None)
            if isinstance(val, str) or isinstance(val, int) or isinstance(val, float):
                result[key] = val
        return result
