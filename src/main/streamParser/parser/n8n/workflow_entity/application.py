import os

from typing import Type, Dict, List
from src.main.streamParser.config import Settings
from src.main.streamParser.exception import StreamParserException
from src.main.streamParser.base.application import Application as BaseApplication
from src.main.streamParser.parser.n8n.workflow_entity.model import Flow, Node, ConnectionEntity


class Application(BaseApplication):
    def __init__(self, settings: Type[Settings], flow: Flow):
        super().__init__(settings)
        self._flow = flow
        self.ignored_node_type: List[str] = ["n8n-nodes-base.stickyNote", "n8n-nodes-base.start"]
        self.attended_node_type: List[str] = [
            "n8n-nodes-base.httpRequest", "n8n-nodes-base.pythonFunction", "n8n-nodes-base.if",
            "n8n-nodes-base.wait", "n8n-nodes-base.pythonAsyncFunction"
        ]
        self.allowed_node_type: List[str] = [*self.ignored_node_type, *self.attended_node_type]

    def find_node_by_node_name(self, node_name: str) -> Node:
        node = next(filter(lambda x: x.name == node_name, self._flow.nodes), None)
        assert node is not None, "nodes中未找到 {} 解析失败 请检查!".format(node_name)
        return node

    def process_connection(self):
        connections: Dict[str, List[ConnectionEntity]] = {
            key: [__ for _ in value.main for __ in _] for key, value in self._flow.connections.items()
        }
        result = {}
        for node_name, connection in connections.items():
            if node_name.lower() == "start":
                node_id = "Start"
            else:
                node = self.find_node_by_node_name(node_name)
                node_id = node.id
            result[node_id] = [
                {"id": self.find_node_by_node_name(_connection.node).id, "name": _connection.node}
                for _connection in connection
            ]
        return result

    def process_function_node(self, node: Node):
        parameters = node.parameters
        function_code = parameters.get("functionCode") or ""
        if not function_code:
            path = os.path.join(self.settings.function_codes_dir, "default.py")
        else:
            path = os.path.join(self.settings.function_codes_dir, "{}.py".format(node.id))
            with open(path, "w") as f:
                f.write(function_code)
        node.parameters["path"] = path
        node.parameters.pop("functionCode", None)

    def process_nodes(self):
        result = []
        for node in self._flow.nodes:
            if node.type in self.ignored_node_type:
                continue
            if node.type not in self.allowed_node_type:
                raise StreamParserException("不合法的node {}".format(node.type), error_code=400)
            if node.type == "n8n-nodes-base.pythonFunction":
                self.process_function_node(node)
            result.append({
                "name": node.name,
                "type": node.type,
                "payload": {"parameters": {
                    **node.parameters, "retryOnFail": node.retryOnFail, "maxTries": node.maxTries,
                    "waitBetweenTries": node.waitBetweenTries, "continueOnFail": node.continueOnFail
                }},
                "id": node.id
            })
        return result

    @property
    def flow(self):
        connections = self.process_connection()
        nodes = self.process_nodes()
        return {"connection": connections, "tasks": nodes}


def get_app(flow: dict):
    return Application(Settings, Flow(**flow))


if __name__ == '__main__':
    import json
    with open("/Users/zyh/mortal/src/main/streamParser/parser/test/data/test_flow.json") as _f:
        with open("/Users/zyh/mortal/src/main/streamActuator/executor/test/data/processed_test_flow.json", "w") as \
                f_write:
            json.dump(get_app(json.load(_f)).flow, f_write, ensure_ascii=False, indent=4)
