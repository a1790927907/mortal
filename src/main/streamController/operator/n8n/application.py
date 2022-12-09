import asyncio

from src.main.streamController.base.application import Application as BaseApplication
from src.main.streamController.external.application import application as external_app


class Application(BaseApplication):
    @staticmethod
    async def process_workflow_entity(entity: dict):
        parsed_result = await external_app.parser_app.parse_stream(
            {"nodes": entity["nodes"], "connections": entity["connections"]}
        )
        return parsed_result

    async def _save_stream_by_reference_id(self, reference_id: int):
        workflow_entity = await external_app.n8n_app.get_workflow_by_id(reference_id)
        parsed_workflow_entity = await self.process_workflow_entity(workflow_entity)
        connection, tasks = parsed_workflow_entity["connection"], parsed_workflow_entity["tasks"]
        connection_id = await external_app.storage_app.upsert_connection({
            "payload": connection, "referenceId": reference_id, "name": workflow_entity["name"]
        })
        store_tasks_request_info = {
            task["id"]: {**task, "connectionId": connection_id} for task in tasks
        }
        await asyncio.gather(*[
            external_app.storage_app.upsert_task({"taskId": task_id, **request_info})
            for task_id, request_info in store_tasks_request_info.items()
        ])
        return {"referenceId": reference_id, "connectionId": connection_id}

    async def save_stream_by_reference_id(self, reference_id: int):
        result = await self._save_stream_by_reference_id(reference_id)
        return {"result": result}
