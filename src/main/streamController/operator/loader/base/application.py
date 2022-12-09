from typing import List, Optional
from src.main.streamController.base.application import Application as BaseApplication


class Application(BaseApplication):
    def rank_connection_payload_task_id(self, connection: dict, key_list: List[str], output: list):
        current = []
        for key in key_list:
            if key not in connection:
                continue
            for payload in connection[key]:
                current.append(payload["id"])
        next_key_list = []
        for c in current:
            if c not in output:
                output.append(c)
                next_key_list.append(c)
        if not next_key_list:
            return
        self.rank_connection_payload_task_id(connection, next_key_list, output)

    def rank_tasks(self, connection: dict, tasks: List[dict]):
        def get_task_by_task_id(task_id: str) -> Optional[dict]:
            for _task in tasks:
                if _task["id"] == task_id:
                    return _task

        result_in_connection, result_not_in_connection, output = [], [], []
        self.rank_connection_payload_task_id(connection, ["Start"], output)
        for t_id in output:
            task_instance = get_task_by_task_id(t_id)
            if task_instance is not None:
                result_in_connection.append(task_instance)
        for task in tasks:
            if task["id"] not in output:
                result_not_in_connection.append(task)
        return {"inExecution": result_in_connection, "outExecution": result_not_in_connection}
