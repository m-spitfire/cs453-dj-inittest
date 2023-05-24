from dataclasses import dataclass
from typing import Any, DefaultDict, List, Dict, Set, Tuple


@dataclass
class APICall:
    method: str
    path: str  # /posts/1
    request_payload: dict  # "{("title", "text"): "example_text"}
    response_expected_data: dict


@dataclass
class APISequence:
    calls: List[APICall]
    param_map: Dict[int, str]
    """
    ```
    param_map[var_name] = (api_idx, data_getter_str)
    ```
    Get data with `data_getter_str` from response of API corresponding to `calls[api_idx]`

    `data_getter_str` e.g. 'data["id"]', 'data[0]["name"]'

    """

    data_map: DefaultDict[str, List[Any]]

    def add_param(self, value) -> str:
        """
        Add a parameter in `param_map`
        @returns `key` where `param_map[key] = value`
        """
        param_cnt = len(self.param_map)
        key = f"${param_cnt}"
        self.param_map[key] = value
        return key

    def add_data(self, new_data_map: DefaultDict[str, List[Any]]):
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


@dataclass
class APIEdgeInfo:
    incoming: List[APINode] = []
    outgoing: List[APINode] = []


APIGraph = Dict[APINode, APIEdgeInfo]
