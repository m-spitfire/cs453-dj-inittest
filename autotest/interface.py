import ast
from dataclasses import dataclass
from typing import Any, DefaultDict, Dict, List, Literal

Method = Literal["GET", "POST"]
ParamMap = dict[str, tuple[int, list[int | str]]]
ResMap = dict[str, ast.Subscript]
Url = ast.Constant | ast.JoinedStr


@dataclass
class Model:
    name: str
    optional: bool = False

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass
class APICall:
    method: str
    path: str  # /posts/1
    request_payload: dict[str, Any]  # "{("title", "text"): "example_text"}
    response_expected_data: dict
    cardinality: int = 0

    def __hash__(self) -> int:
        path = self.path.strip("/")

        if self.cardinality == 0:
            return hash(f"{self.method} {path}")

        return hash(f"{self.method} {path}{self.cardinality}")


@dataclass
class APISequence:
    calls: List[APICall]
    param_map: ParamMap
    data_map: DefaultDict[str, List[Any]]
    """
    ```
    param_map[var_name] = (api_idx, data_getter_str)
    ```
    Get data with `data_getter_str` from response of API corresponding to `calls[api_idx]`

    `data_getter_str` e.g. 'data["id"]', 'data[0]["name"]'

    """

    def add_param(self, value) -> str:
        """
        Add a parameter in `param_map`
        @returns `key` where `param_map[key] = value`
        """
        param_cnt = len(self.param_map)
        key = f"${param_cnt}"

        if value == 0:
            value = (-1, [])

        self.param_map[key] = value
        return key

    def add_data(self, new_data_map: DefaultDict[str, list[Any]]):
        for key, value in new_data_map.items():
            self.data_map[key].extend(value)


@dataclass
class API:
    method: str
    path: str
    creates: List[Model]  # outgoing
    uses: List[Model]  # incoming (prerequisite)
    request_type: dict
    response_type: dict
    cardinality: int = 0

    def __hash__(self) -> int:
        path = self.path.strip("/")

        if self.cardinality == 0:
            return hash(f"{self.method} {path}")

        return hash(f"{self.method} {path} ({self.cardinality})")

    def __repr__(self) -> str:
        if self.cardinality == 0:
            return f"{self.method} {self.path}"

        return f"{self.method} {self.path} ({self.cardinality})"


@dataclass
class Node:
    def __init__(self, label: str):
        self.label = label

    def __repr__(self) -> str:
        return str(self.label)

    def __hash__(self) -> int:
        return hash(str(self.label))

    def __eq__(self, __value: object) -> bool:
        return self.label == __value.label


@dataclass
class CondNode(Node):
    def __init__(self, label: str, users=[], creators=[]):
        self.label = label
        # self.users = users
        # self.creators = creators

    def __hash__(self) -> int:
        return hash(self.label)


@dataclass
class ConvNode(Node):
    def __init__(
        self,
        label: str,
        meta: Any,
        uses: List[CondNode] = [],
        creates: List[CondNode] = [],
    ):
        self.label = label
        self.uses = uses
        self.creates = creates
        self.meta = meta

        if len(uses) == 0:
            self.uses = []

        if len(creates) == 0:
            self.creates = []

    def __hash__(self) -> int:
        return hash(self.label)


CondNode.users: List[ConvNode]
CondNode.creators: List[ConvNode]


@dataclass
class CondGraph:
    cond_nodes: Dict[str, CondNode]
    conv_nodes: Dict[str, ConvNode]

    def check(self):
        print("conditions:")
        for condition in self.cond_nodes.values():
            print(f"{condition.label}")

        print("vertices:")
        for vertex in self.conv_nodes.values():
            print(
                f"{vertex.label} (creates: {len(vertex.creates)} / uses: {len(vertex.uses)})"
            )


class ConvSequence:
    vertices: List[ConvNode]

    def __init__(self, vertices) -> None:
        self.vertices = vertices

    def __hash__(self) -> int:
        return hash(str(self))

    def __repr__(self) -> str:
        labels = [vertex.label for vertex in self.vertices]
        return " -> ".join(labels)

    def __eq__(self, __value: object) -> bool:
        for my_vertex in self.vertices:
            for their_vertex in __value.vertices:
                if my_vertex != their_vertex:
                    return False
        return True
