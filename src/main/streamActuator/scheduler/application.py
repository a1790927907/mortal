import time
import asyncio
import traceback

from src.main.utils.logger import logger
from aiokafka.cluster import ClusterMetadata
from typing import Type, List, Optional, Any, Dict
from src.main.streamActuator.config import Settings
from src.main.utils.time_utils import get_now_string
from src.main.streamActuator.model import Task, Connection
from src.main.utils.kafka_utils import fetch_kafka_metadata
from src.main.utils.data_process_utils import validate_model
from src.main.streamActuator.exception import StreamActuatorException
from src.main.streamActuator.base.application import Application as BaseApplication
from src.main.streamActuator.executor.wait.application import get_app as get_wait_executor
from src.main.streamActuator.executor.http.application import get_app as get_http_executor
from src.main.streamActuator.executor.branch.application import get_app as get_branch_executor
from src.main.streamActuator.executor.function.application import get_app as get_function_executor
from src.main.streamActuator.recorder.worker.application import application as recorder_worker_app
from src.main.streamActuator.scheduler.model import ExecutionParameters, ToBeExecutedTask, ExecutionCondition, \
    Upstream, TaskStatus, Condition


class Application(BaseApplication):
    partition_info: Dict[str, List[int]] = {}

    def __init__(self, settings: Type[Settings], parameters: ExecutionParameters):
        super().__init__(settings)
        self.parameters = parameters
        self.executor_mappings = {
            "n8n-nodes-base.httpRequest": get_http_executor,
            "n8n-nodes-base.pythonFunction": get_function_executor,
            "n8n-nodes-base.if": get_branch_executor,
            "n8n-nodes-base.wait": get_wait_executor,
            "n8n-nodes-base.pythonAsyncFunction": get_function_executor
        }
        self.ignored_status_task_type = ["n8n-nodes-base.stickyNote", "n8n-nodes-base.start"]
        self.tasks: Dict[str, asyncio.Task] = {}
        self.queue = recorder_worker_app.queue
        self.execution_time: Optional[float] = None
        self.tasks_running_partition: Optional[int] = None
        self.tasks_run_start_time: Optional[str] = None
        self.tasks_run_end_time: Optional[str] = None

    async def select_partition(self, topic: str, *, metadata: Optional[ClusterMetadata] = None) -> int:
        if metadata is None:
            metadata = await fetch_kafka_metadata(self.settings.kafka_server)
        partitions = metadata.partitions_for_topic(topic)
        if topic not in self.partition_info:
            self.partition_info[topic] = []
        for candidate_partition in partitions:
            if candidate_partition not in self.partition_info[topic]:
                self.partition_info[topic].append(candidate_partition)
                return candidate_partition
        self.partition_info[topic] = []
        result = await self.select_partition(topic, metadata=metadata)
        return result

    @property
    def running_status(self):
        for status in self.parameters.taskStatus:
            if status in ["failedNotContinue"]:
                return "failed"
            elif status == "skip" and status.errorMessage:
                return "warning"
        return "success"

    def record_tasks_running(self):
        if not self.parameters.record.require:
            return
        message = {
            "id": self.parameters.record.tasksRunningId, "connectionId": self.parameters.connection.id,
            "statusPayload": {"taskStatus": [status.dict() for status in self.parameters.taskStatus]},
            "contextPayload": self.parameters.context
        }
        self.queue.put_nowait({
            "type": "saveTasksRunning", "message": message, "messageConfig": {"partition": self.tasks_running_partition}
        })

    def remove_tasks_running(self):
        if not self.parameters.record.require:
            return
        message = {"id": self.parameters.record.tasksRunningId}
        self.queue.put_nowait({
            "type": "deleteTasksRunning", "message": message,
            "messageConfig": {"partition": self.tasks_running_partition}
        })

    def get_task_by_task_id(self, task_id: str) -> Task:
        for task in self.parameters.tasks:
            if task.id == task_id:
                return task
        raise StreamActuatorException("不存在task: {}".format(task_id), error_code=404)

    def extract_executed_tasks(self) -> List[ToBeExecutedTask]:
        result: List[ToBeExecutedTask] = []
        for upstream_task_id, tasks in self.parameters.connection.payload.items():
            if upstream_task_id.lower() == "start":
                upstream_task = Task(
                    id=upstream_task_id, name="Start", type="n8n-nodes-base.start", payload={"parameters": {}}
                )
            else:
                upstream_task = self.get_task_by_task_id(upstream_task_id)
            if upstream_task.type == "n8n-nodes-base.if":
                execution_condition = ExecutionCondition(
                    **{"type": "if", "condition": {"value": False, "factor": "is"}}
                )
            elif upstream_task.type == "n8n-nodes-base.wait":
                execution_condition = ExecutionCondition(
                    **{"type": "wait", "condition": {"value": True, "factor": "is"}}
                )
            elif upstream_task.type == "n8n-nodes-base.start":
                execution_condition = ExecutionCondition(type="nowait")
            else:
                execution_condition = ExecutionCondition(
                    **{"condition": {"value": ["success", "failedAndContinue"], "factor": "in"}}
                )
            for index, task in enumerate(tasks):
                if index == 0 and upstream_task.type == "n8n-nodes-base.if":
                    execution_condition = ExecutionCondition(
                        **{"type": "if", "condition": {"value": True, "factor": "is"}}
                    )
                elif index == 1 and upstream_task.type == "n8n-nodes-base.if":
                    execution_condition = ExecutionCondition(
                        **{"type": "if", "condition": {"value": False, "factor": "is"}}
                    )
                upstream = Upstream(task=upstream_task, executionCondition=execution_condition)
                task_in_result = next(filter(lambda x: x.task.id == task.id, result), None)
                if task_in_result is not None:
                    task_in_result.upstreams.append(upstream)
                else:
                    task_instance = self.get_task_by_task_id(task.id)
                    result.append(ToBeExecutedTask(upstreams=[upstream], task=task_instance))
        return result

    def get_task_status_by_task_id(self, task_id: str) -> Optional[TaskStatus]:
        for task_status in self.parameters.taskStatus:
            if task_status.id == task_id:
                return task_status

    def set_task_status(
            self, status: str, task: Task, *, error_message: Optional[str] = None, start_time: Optional[str] = None,
            end_time: Optional[str] = None, retry_time: Optional[int] = None, **kwargs
    ):
        task_status = self.get_task_status_by_task_id(task.id)
        if task_status is None:
            self.parameters.taskStatus.append(
                TaskStatus(
                    id=task.id, name=task.name, status=status, errorMessage=error_message, startTime=start_time,
                    endTime=end_time, retryTime=retry_time or 0, **kwargs
                )
            )
        else:
            task_status.status = status
            if error_message is not None:
                task_status.errorMessage = error_message
            if start_time is not None:
                task_status.startTime = start_time
            if end_time is not None:
                task_status.endTime = end_time
            if retry_time is not None:
                task_status.retryTime = retry_time
            for key, value in kwargs.items():
                if value is None:
                    continue
                if hasattr(task_status, key):
                    setattr(task_status, key, value)
            validate_model(task_status)

    async def execute_task(self, task: Task):
        executor = self.executor_mappings[task.type](task.dict(), self.parameters.context)
        try:
            self.set_task_status("pending", task, start_time=get_now_string(), retry_time=executor.retry_time)
            self.record_tasks_running()
            await executor.execute_task()
            self.set_task_status("success", task, end_time=get_now_string(), retry_time=executor.retry_time)
            self.parameters.context[task.name] = executor.result
            self.record_tasks_running()
            return
        except StreamActuatorException as e:
            logger.error(e.message)
            error_message = e.message
        except Exception as e:
            logger.exception(e)
            error_message = traceback.format_exc()
        finally:
            self.parameters.context[task.name] = executor.result
        if not task.payload.parameters.get("continueOnFail"):
            status = "failedNotContinue"
        else:
            status = "failedAndContinue"
        self.set_task_status(
            status, task, error_message=error_message, end_time=get_now_string(), retry_time=executor.retry_time
        )
        self.record_tasks_running()

    @staticmethod
    def handle_condition(source: Any, condition: Condition) -> bool:
        if condition.factor == "is":
            return source is condition.value
        elif condition.factor == "in":
            return source in condition.value
        elif condition.factor == "eq":
            return source == condition.value
        elif condition.factor == "gt":
            return source > condition.value
        elif condition.factor == "lt":
            return source < condition.value
        elif condition.factor == "gte":
            return source >= condition.value
        elif condition.factor == "lte":
            return source <= condition.value
        else:
            raise StreamActuatorException("invalid condition factor -> {}".format(condition.dict()), error_code=400)

    def collect_tasks_to_be_executed(self, tasks: List[ToBeExecutedTask]):
        result: List[Task] = []
        for task_to_be_executed in tasks:
            for upstream in task_to_be_executed.upstreams:
                if upstream.executionCondition.type == "nowait":
                    result.append(task_to_be_executed.task)
                    break
                elif upstream.executionCondition.type == "status":
                    status = self.get_task_status_by_task_id(upstream.task.id)
                    status = status.status if status is not None else None
                    if not self.handle_condition(status, upstream.executionCondition.condition):
                        break
                elif upstream.executionCondition.type == "if" or upstream.executionCondition.type == "wait":
                    if upstream.task.name in self.parameters.context:
                        task_result = self.parameters.context[upstream.task.name]["value"]
                        if not self.handle_condition(task_result, upstream.executionCondition.condition):
                            break
                    else:
                        break
                else:
                    break
            else:
                result.append(task_to_be_executed.task)
        return result

    def set_task_status_and_downstream_task(self, status: str, task: Task, *, overwrite_status: Optional[str] = None):
        self.set_task_status(overwrite_status or status, task)
        if task.id in self.parameters.connection.payload:
            for next_task in self.parameters.connection.payload[task.id]:
                next_task_status = self.get_task_status_by_task_id(next_task.id)
                self.set_task_status_and_downstream_task(
                    status, self.get_task_by_task_id(next_task.id),
                    overwrite_status=next_task_status.status if next_task_status is not None else None
                )

    def supplement_task_status(self, tasks_to_be_executed: List[ToBeExecutedTask]):
        def search_upstream_tasks(task_id: str) -> Optional[List[Upstream]]:
            for task_to_be_executed in tasks_to_be_executed:
                if task_to_be_executed.task.id == task_id:
                    return task_to_be_executed.upstreams

        for task in self.parameters.tasks:
            if task.type in self.ignored_status_task_type:
                continue
            status = self.get_task_status_by_task_id(task.id)
            if status is None:
                upstream_tasks = search_upstream_tasks(task.id)
                if upstream_tasks is None:
                    self.parameters.taskStatus.append(TaskStatus(
                        id=task.id, name=task.name, status="skip", errorMessage="no upstream task"
                    ))
                else:
                    for upstream_task in upstream_tasks:
                        if upstream_task.task.type == "n8n-nodes-base.if":
                            self.set_task_status_and_downstream_task("skip", task)
                            break
                    else:
                        self.set_task_status("skip", task, error_message="not execute")

    def log_after_schedule_finish(self):
        result = []
        for task_id in self.tasks:
            task = self.get_task_by_task_id(task_id)
            result.append({
                "task": task,
                "status": self.get_task_status_by_task_id(task_id),
                "result": self.parameters.context.get(task.name) or {}
            })
        message, message_template = "", "任务: {} 状态: {}, 开始时间: {}, 结束时间: {}, 重试次数: {}, 耗时: {}"
        for index, instance in enumerate(result):
            message += message_template.format(
                instance["task"].name, instance["status"].status if instance["status"] else "无状态",
                instance["status"].startTime, instance["status"].endTime, instance["status"].retryTime,
                instance["result"]["executeTime"] if instance["result"].get("executeTime") is not None else "???" + " 秒"
            )
            if instance["status"] and "fail" in instance["status"].status:
                message += " 错误信息: {}".format(instance["status"].errorMessage)
            if index != len(result) - 1:
                message += "\n"
        long_line = "-" * 50
        logger.info("\n{}\n执行结束, 执行细节如下:\n{}\n{}".format(long_line, message, long_line))

    def collect_initial_tasks_from_status(self):
        for task_status in self.parameters.taskStatus:
            if task_status.status in ["failedAndContinue", "success", "failedNotContinue"]:
                self.tasks[task_status.id] = asyncio.create_task(asyncio.sleep(0))

    def remove_invalid_initial_task_status(self):
        for status in self.parameters.taskStatus.copy():
            try:
                self.get_task_by_task_id(status.id)
            except StreamActuatorException as _e:
                self.parameters.taskStatus.remove(status)

    def _schedule_after_collect_task(self) -> bool:
        if not self.tasks:
            return True
        for task_key, task_instance in self.tasks.items():
            if not task_instance.done():
                break
        else:
            return True
        return False

    async def _schedule_connection(self):
        tasks_to_be_executed = self.extract_executed_tasks()
        self.remove_invalid_initial_task_status()
        self.collect_initial_tasks_from_status()
        while True:
            collected_tasks = self.collect_tasks_to_be_executed(tasks_to_be_executed)
            for collected_task in collected_tasks:
                if collected_task.id not in self.tasks:
                    logger.info("开始执行task -> name: {}, id: {}".format(collected_task.name, collected_task.id))
                    self.tasks[collected_task.id] = asyncio.create_task(self.execute_task(collected_task))
            if self._schedule_after_collect_task():
                break
            await asyncio.sleep(0)
        self.supplement_task_status(tasks_to_be_executed)
        self.log_after_schedule_finish()

    async def schedule_connection(self):
        now = time.time()
        self.tasks_run_start_time = get_now_string()
        self.tasks_running_partition = await self.select_partition(
            self.settings.kafka_monitor_tasks_running_worker_topic
        )
        self.parameters.context["Start"] = {"value": self.parameters.input}
        await self._schedule_connection()
        self.execution_time = time.time() - now
        self.tasks_run_end_time = get_now_string()


def get_app(
        tasks: List[dict], connection: dict, input_value: dict, *, context: Optional[dict] = None,
        task_status: Optional[List[dict]] = None, record: Optional[dict] = None
):
    params = {"tasks": [Task(**task) for task in tasks], "connection": Connection(**connection), "input": input_value}
    if context:
        params.update(context=context)
    if task_status:
        params.update(taskStatus=[TaskStatus(**status) for status in task_status])
    if record:
        params.update(record=record)
    return Application(Settings, ExecutionParameters(**params))


if __name__ == '__main__':
    import json

    with open("/Users/zyh/mortal/src/main/streamActuator/executor/test/data/processed_test_flow.json") as f:
        data = json.load(f)
    _app = get_app(data["tasks"], {"id": "", "referenceId": "1", "payload": data["connection"]}, input_value={
        "entityId": "test12223",
        "tenant": "mesoor-98",
        "entitType": "Resume",
        "schema": "https://transmitter-schema.nadileaf.com/v2/publish/entity/standard/Resume/version/v_2.0."
                  "167#/properties/data"
    }, task_status=[
        {
            "id": "b005ee63-ca8e-49e8-ab53-a27834725dbf",
            "name": "getResume",
            "status": "failedAndContinue",
            "errorMessage": "请求 https://transmitter.nadileaf.com/v2/entity/mesoor-98/Resume/test12223 失败 status: 404 response: {\"message\":\"entity not found\"}"
        },
        {
            "id": "55486eba-5b91-40f0-b9c3-560f2aa4a9fb",
            "name": "IF",
            "status": "success"
        }
    ], context={'Start': {'value': {'entityId': 'test12223', 'tenant': 'mesoor-98', 'entitType': 'Resume', 'schema': 'https://transmitter-schema.nadileaf.com/v2/publish/entity/standard/Resume/version/v_2.0.167#/properties/data'}}, 'getResume': {'value': {'message': 'entity not found'}, 'extraValue': {'status': 404, 'url': 'https://transmitter.nadileaf.com/v2/entity/mesoor-98/Resume/test12223'}, 'executeTime': 0.14846110343933105}, 'IF': {'value': False, 'extraValue': {}, 'executeTime': 0.001123189926147461}, 'logAllWhenNoResume': {'value': {}, 'extraValue': {'status': 200, 'url': 'http://localhost:11000/log'}, 'executeTime': 0.003907918930053711}})
    # for _ in _app.extract_executed_tasks():
    #     print(json.dumps(_.dict(), ensure_ascii=False, indent=4))
    #     print("-" * 50)
    asyncio.run(_app.schedule_connection())
    # for s in _app.parameters.taskStatus:
    #     print(json.dumps(s.dict(), ensure_ascii=False, indent=4))
    # print(_app.parameters.context)
