import time

from src.main.streamActuator.config import Settings
from src.main.streamActuator.scheduler.application import get_app
from src.main.streamActuator.integration.model import RequestInfo
from src.main.streamActuator.base.application import Application as BaseApplication
from src.main.streamActuator.scheduler.application import Application as SchedulerApplication
from src.main.streamActuator.recorder.worker.application import application as recorder_worker_app


class Application(BaseApplication):
    @staticmethod
    def record_tasks_run(schedule_app: SchedulerApplication):
        message = {
            "id": schedule_app.parameters.record.tasksRunId, "input": schedule_app.parameters.input,
            "executeTime": schedule_app.execution_time, "status": schedule_app.running_status,
            "connectionId": schedule_app.parameters.connection.id,
            "openid": schedule_app.parameters.record.tasksRunOpenid,
            "startTime": schedule_app.tasks_run_start_time, "endTime": schedule_app.tasks_run_end_time
        }
        recorder_worker_app.queue.put_nowait({"type": "saveTasksRun", "message": message})
        return message["id"]

    @staticmethod
    def record_task_status(schedule_app: SchedulerApplication, run_id: str):
        messages = []
        for status in schedule_app.parameters.taskStatus:
            context = schedule_app.parameters.context.get(status.name) or {}
            output_value, output_extra = context.get("value"), context.get("extraValue")
            if not output_value and not output_extra:
                output = None
            else:
                output = {"data": output_value, "extra": output_extra or {}}
            messages.append({
                "status": status.status, "runId": run_id, "taskId": status.id,
                "executeTime": context.get("executeTime"), "errorMessage": status.errorMessage, "output": output,
                "retryTime": status.retryTime, "startTime": status.startTime, "endTime": status.endTime
            })
        for message in messages:
            recorder_worker_app.queue.put_nowait({"type": "saveTaskStatus", "message": message})

    @staticmethod
    def record_tasks_running_mapping(schedule_app: SchedulerApplication, run_id: str):
        schedule_app.queue.put_nowait({"type": "saveTasksRunningMapping", "message": {
            "redisKey": schedule_app.parameters.record.tasksRunningId, "tasksRunId": run_id
        }})

    def record_after_schedule(self, schedule_app: SchedulerApplication):
        if not schedule_app.parameters.record.require:
            return
        tasks_run_id = self.record_tasks_run(schedule_app)
        self.record_task_status(schedule_app, run_id=tasks_run_id)
        schedule_app.remove_tasks_running()
        self.record_tasks_running_mapping(schedule_app, run_id=tasks_run_id)

    @staticmethod
    def get_scheduler_app(request_info: RequestInfo):
        return get_app(
            [task.dict() for task in request_info.tasks],
            request_info.connection.dict(), input_value=request_info.input, context=request_info.context,
            task_status=request_info.taskStatus, record=request_info.record
        )

    async def _schedule_connection(self, request_info: RequestInfo):
        now = time.time()
        app = self.get_scheduler_app(request_info)
        await app.schedule_connection()
        self.record_after_schedule(app)
        return {
            "status": [
                status.dict() for status in app.parameters.taskStatus
            ],
            "context": app.parameters.context, "cost": time.time() - now
        }

    async def schedule_connection(self, request_info: RequestInfo):
        result = await self._schedule_connection(request_info)
        return {"result": result}


application = Application(Settings)
