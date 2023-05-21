"""
Generate sequences that ends with each and every API call
"""

from collections import deque, defaultdict
from dataclasses import dataclass
from typing import DefaultDict, List, Dict, Set, Tuple
from .apis import apis, APINode
from jsf import JSF


@dataclass
class APICall:
    method: str
    path: str  # /posts/1
    request_payload: dict  # "{("title", "text"): "example_text"}
    response_expected_data: dict


"""
Examples:
target:
APICall(
    method="GET",
    path="/posts/$1",
    request_payload={},
    response_expected_data=...
)

sequence:
APISequence(
    calls=[
        APICall(method="POST, path="users/", request_payload={...}),
        APICall(method="POST, path="posts/", request_payload={...}),
        APICall(method="GET, path="posts/$1/", request_payload={})
    ],
    param_map = {"$1": (1, 'data["id"]')} # Get data with data["id"]from response of API corresponding to calls[1]
)

expected outcome:
def test_get_post():
    res0 = client.post("users/")
    res1 = client.post("posts/")
    res2 = client.get(f"posts/{res1.data.id}")

"""


@dataclass
class APISequence:
    calls: List[APICall]
    param_map: Dict[Tuple[int, str]]
    """
    ```
    param_map[var_name] = (api_idx, data_getter_str)
    ```
    Get data with `data_getter_str` from response of API corresponding to `calls[api_idx]`

    `data_getter_str` e.g. 'data["id"]', 'data[0]["name"]'

    """

    def add_param(self, value):
        param_cnt = len(self.param_map)
        key = f"${param_cnt}"
        self.param_map[key] = value
        return key


def find_trace(obj, criteria) -> list[str | int]:
    trace = []

    def helper(obj, criteria):
        if type(obj) == list:
            for i, e in enumerate(obj):
                value = helper(e, criteria)
                if value:
                    trace.append(i)
                    return value

        if type(obj) == dict:
            for key in obj:
                if type(key) not in [list, dict] and criteria(key):
                    trace.append(key)
                    return obj[key]
                else:
                    value = helper(obj[key], criteria)
                    if value:
                        trace.append(key)
                        return value

    helper(obj, criteria)
    return trace


def find(obj, criteria):
    if type(obj) == list:
        for _, e in enumerate(obj):
            value = find(e, criteria)
            if value:
                return value

    if type(obj) == dict:
        for key in obj:
            if type(key) not in [list, dict] and criteria(key):
                return obj[key]
            else:
                value = find(obj[key], criteria)
                if value:
                    return value

    return None


def predict(obj, sequence: APISequence):
    def lookup(field):
        """
        필드 이름만 같으면 그대로 사용
        """
        for call in reversed(sequence.calls):
            value = find(call.response_expected_data, lambda key: key == field)
            if value is not None:
                return value

        return None

    def visit(obj):
        if type(obj) == list:
            for i, e in enumerate(obj):
                if type(e) not in [list, dict]:
                    v = lookup(e)
                    if v is not None:
                        obj[i] = v
                else:
                    visit(e)
            return

        if type(obj) == dict:
            for field in obj:
                if type(field) not in [list, dict]:
                    v = lookup(field)
                    if v is not None:
                        obj[field] = v
                else:
                    visit(obj[field])
            return

    visit(obj)


def trace_to_value(trace: list[str | int], accessor="data"):
    """
    e.g. 1
    data[0]["examples"]["name"]

    e.g. 2
    data["student"]["id_card_type"]
    """

    access_stmt = [accessor]
    for cur in reversed(trace):
        if type(cur) == str:
            access_stmt.append(f'["{cur}"]')
        else:
            access_stmt.append(f"[{cur}]")

    return "".join(access_stmt)


def predict_id(model_name, sequence: APISequence):
    # type이 model_name인 id 찾아오기
    """
    response type 중 model_name에 해당하는 model의 key를 값으로 하는
    field가 있으면 해당 값 사용
    """

    def lookup():
        for call in reversed(sequence.calls):
            access_trace = find_trace(
                call.response_expected_data, lambda key: key.startswith(model_name)
            )
            if access_trace is not None:
                return trace_to_value(access_trace)

        return 0

    value = lookup()
    return sequence.add_param(value)


def generate_call(target: APINode, sequence: APISequence):
    """
    To call target API, generate request payload data / expected response data
    which fit in given type with previous API calls so far

    Data generation heuristics
    1) Information used recently is likely to be used again
    2) Information in response is more likely to be used than information in request

    <Model>::<Field name> = the field is id of model

    $로 시작하는건 map에서 조회
    """
    routes = []
    for route in target.path.split("/"):
        splitted = [v for v in route.split(":") if len(v) > 0]
        _, model_name, _ = splitted  # e.g. ["int", "User", "pk"]
        key = predict_id(model_name, sequence)
        routes.append(key)

    routes.append("")
    path = "/".join(routes)

    request_faker = JSF(target.request_type)
    faked_request = request_faker.generate()  # User로 시작하는지는 어떻게 알지?

    predict(faked_request, sequence, drop_type=True)

    call = APICall(
        method=target.method,
        path=path,
        request_payload=faked_request,
        response_expected_data={},
    )

    sequence.calls.append(call)

    response_faker = JSF(target.response_type)
    faked_response = response_faker.generate()

    predict(faked_response, sequence, drop_type=False)

    sequence.calls[-1].response_expected_data = faked_response


@dataclass
class APIEdgeInfo:
    incoming: List[APINode] = []
    outgoing: List[APINode] = []


APIGraph = Dict[APINode, APIEdgeInfo]


def get_requirements(target: APINode, graph) -> Set[APINode]:
    requirements = set()
    queue = deque([target])

    while queue:
        node = queue.popleft()
        requirements.add(node)
        queue.extend(graph[node].incoming)

    return requirements


def generate_sequences(target: APINode, graph: APIGraph) -> List[APICall]:
    """
    For each API, generate a sequence of API calls
    which resolve all dependency and ends with the target API

    Use topological sort algorithm

    dependers[node1] = [node2] : node2 depends on node1

    Assumption: at most one create for each API
    Generate a call sequence for the target API only

    target API 만 만들기
    """
    requirements = get_requirements(target, graph)
    in_degrees = defaultdict(int)
    call_sequence = APISequence()
    queue = deque([])

    for node in requirements:
        in_degrees[node] = len(graph[node].incoming)
        if in_degrees[node] == 0:
            queue.append(node)

    while len(queue) > 0:
        target = queue.popleft()
        generate_call(target, call_sequence)

        for depender in graph[target].outgoing:
            if depender not in requirements:
                continue

            in_degrees[depender] -= 1
            if in_degrees[depender] == 0:
                queue.append(depender)

    return call_sequence


def has_cycle(graph: APIGraph):
    visited = 0
    queue = deque([])
    in_degrees = defaultdict(int)

    for node in graph:
        in_degrees[node] = len(graph[node].incoming)
        if in_degrees[node] == 0:
            queue.append(node)

    while queue:
        node = queue.popleft()
        visited += 1

        for child in graph[node].outgoing:
            in_degrees[child] -= 1
            if in_degrees[child] == 0:
                queue.append(child)

    return visited != len(graph.keys())


def resolve_cycle(graph: APIGraph):
    """
    TODO:
    """
    print("the graph has cycle")
    exit(-1)


def generate_all_sequences(apis: List[APINode]) -> Dict[APINode, List[List[APICall]]]:
    """
    Warning: Extremely inefficient

    For each API, generate ALL sequences of API calls
    which resolve all dependency and ends with the target API

    Dependencies between APIs are solely determined by the list of Models
    which the API `creates` and `uses`

    TODO: Add cache
    """
    graph = {node: APIEdgeInfo() for node in apis}
    creators = defaultdict(list)
    users = defaultdict(list)

    for node in apis:
        for model in node.creates:
            creators[model].append(node)
        for model in node.uses:
            users[model].append(node)

    # TODO: generate multiple graphs from multiple creates
    for model in creators:
        dependency = creators[model][0]
        for depender in users[model]:
            graph[dependency].outgoing.append(depender)
            graph[depender].incoming.append(dependency)

    if has_cycle(graph):
        resolve_cycle(graph)

    call_sequences = defaultdict(list)
    for node in apis:
        sequence = generate_sequences(node, graph)
        call_sequences[node].append(sequence)

    call_sequences.drop_type()
    return call_sequences


print(generate_all_sequences(apis))
