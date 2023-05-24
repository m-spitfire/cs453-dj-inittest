"""
Generate sequences that ends with each and every API call
"""
from collections import defaultdict
from typing import List, Dict
from autotest.graph import build_graph, get_requirements
from autotest.infer import infer, infer_id
from autotest.interface import APICall, APIGraph, APISequence, APINode
from autotest.apis import apis
from autotest.utils import get_cleaned_key


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
        key = infer_id(model_name, sequence)
        routes.append(key)

    routes.append("")
    path = "/".join(routes)

    inferred_req, inferred_req_map = infer(target.request_type, sequence)
    sequence.add_data(inferred_req_map)

    inferred_res, inferred_res_map = infer(target.request_type, sequence)
    sequence.add_data(inferred_res_map)

    sequence.calls.append(
        APICall(
            method=target.method,
            path=path,
            request_payload=inferred_req,
            expected_response_data=inferred_res,
        )
    )


def remove_model_prefix(data):
    def helper(original):
        if isinstance(original, dict):
            new_items = []
            for key in original.keys():
                new_value = helper(original[key])
                new_key = get_cleaned_key(key)
                new_items.append((new_key, new_value))
            return dict(new_items)
        elif isinstance(original, list):
            new_values = []
            for item in original:
                new_value = helper(item)
                new_values.append(new_value)
            return new_values

        return original

    return helper(data)


def generate_all_sequences(graph: APIGraph) -> Dict[APINode, List[APISequence]]:
    """
    Warning: Extremely inefficient

    Basically equivalent to generate all path from graph

    For each API, generate ALL sequences of API calls
    which resolve all dependency(=incoming edge) and ends with the target API

    TODO: Add cache
    """
    call_sequences = defaultdict(list)
    for target in graph.keys():
        # single path ends with target
        requirements = get_requirements(target, graph)
        sequence = APISequence()
        for node in requirements:
            generate_call(node, sequence)

        for call in sequence.calls:
            call.request_payload = remove_model_prefix(call.request_payload)

        call_sequences[target].append(sequence)

    return call_sequences


graph = build_graph(apis)
print(generate_all_sequences(graph))
