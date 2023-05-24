import ast
from dataclasses import dataclass
from typing import Any, DefaultDict, Literal

Method = Literal["GET", "POST"]
ParamMap = dict[str, tuple[int, list[int | str]]]
ResMap = dict[str, ast.Subscript]
Url = ast.Constant | ast.JoinedStr


@dataclass
class APICall:
    method: str
    path: str  # /posts/1
    request_payload: dict[str, Any]  # "{("title", "text"): "example_text"}
    response_expected_data: dict

    def __hash__(self) -> int:
        return hash(self.path.strip("/") + self.method)


@dataclass
class APISequence:
    calls: list[APICall]
    param_map: ParamMap
    data_map: DefaultDict[str, list[Any]]
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
class APINode:
    method: str
    path: str
    creates: list[str]
    uses: list[str]
    request_type: dict
    response_type: dict

    def __hash__(self) -> int:
        return f"{self.method} {self.path}".__hash__()

    def __repr__(self) -> str:
        return f'"{self.method} {self.path}"'


@dataclass
class APIEdgeInfo:
    incoming: list[APINode]
    outgoing: list[APINode]


APIGraph = dict[APINode, APIEdgeInfo]
