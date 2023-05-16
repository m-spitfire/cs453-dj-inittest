"""
Generate sequences that ends with each and every API call
"""

from collections import deque, defaultdict
from dataclasses import dataclass
from typing import DefaultDict, List, Dict


@dataclass
class APINode:
    method: str
    path: str
    creates: list[str]
    uses: list[str]
    request_type: dict[str, str]
    response_type: dict[str, str]


@dataclass
class APICall:
    method: str
    path: str  # /posts/1
    request_payload: dict  # "{("title", "text"): "example_text"}
    response_expected_data: dict


def fake(field):
    _, ty = field
    if ty == "int":
        return 0

    return "fake_text"


def lookup(field, data):
    _, field_type = field
    if field in data.keys():
        return data[field]

    for name, ty in data:
        value = data[(name, ty)]
        if field_type == ty:
            return value

    return None


def predict(field, calls: List[APICall]):
    for call in reversed(calls):
        value = lookup(field, call.response_expected_data)
        if value is not None:
            return value

        value = lookup(field, call.request_payload)
        if value is not None:
            return value

    return fake(field)


def generate_call(target: APINode, calls: List[APICall]):
    """
    To call target API, generate request payload data / expected response data
    which fit in given type with previous API calls so far

    Data generation heuristics
    1) Information used recently is likely to be used again
    2) Information in response is more likely to be used than information in request

    TODO: handle path param
    """

    payload = {}
    for field in target.request_type:
        payload[field] = predict(field, calls)

    call = APICall(
        method=target.method,
        path=target.path,
        request_payload=payload,
        response_expected_data={},
    )

    expected_data = {}
    for field in target.response_type:
        expected_data[field] = predict(field, calls + [call])

    call.response_expected_data = expected_data
    return call


def generate_sequences(
    apis: List[APINode], dependers: DefaultDict[list], in_degrees: DefaultDict[int]
) -> Dict[APINode, List[APICall]]:
    """
    For each API, generate a sequence of API calls
    which resolve all dependency and ends with the target API

    Use topological sort algorithm

    dependers[node1] = [node2] : node2 depends on node1
    """

    call_sequences = {}
    queue = deque()

    for target in apis:
        for dependency in target.uses:
            dependers[dependency].append(target)
        in_degrees[target] = len(target.uses)

    while len(queue) > 0:
        target, calls = queue.popleft()
        target_call = generate_call(target, calls)
        call_sequences[target] = calls + target_call

        for depender in dependers[target]:
            in_degrees[depender] -= 1
            if in_degrees[depender] == 0:
                queue.append((depender, call_sequences[target_call]))

    return call_sequences


def generate_all_sequences(apis: List[APINode]) -> Dict[APINode, List[List[APICall]]]:
    """
    For each API, generate ALL sequences of API calls
    which resolve all dependency and ends with the target API

    Dependencies between APIs are soley determined by the list of Models
    which the API `creates` and `uses`

    TODO: generate dependency graph from list of models
    TODO: handle cycle
    TODO: handle multiple creates
    """

    pass


apis = [
    APINode("GET", "/posts/", [], [], {}, {}),
    APINode(
        "POST",
        "/posts/",
        [""],
        [],
        {"title": "text", "content": "text", "author": "user_id"},
        {},
    ),
    APINode("GET", "/users/", [], [], {}, {}),
    APINode("POST", "/users/", [], [], {}, {}),
]

print(generate_all_sequences(apis))
