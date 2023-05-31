"""
Generate sequences that ends with each and every API call
"""
from collections import defaultdict
from typing import List, Dict
from graph import build_graph, iter_path
from infer import infer, infer_id
from interface import APICall, APISequence, API, CondGraph
from utils import get_cleaned_key
from itertools import combinations


def generate_call(target: API, sequence: APISequence):
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
        if len(splitted) == 0:
            continue
        if len(splitted) < 3:
            routes.append(splitted[0])
            continue

        _, model_name, _ = splitted  # e.g. ["int", "User", "pk"]
        key = infer_id(model_name, sequence)
        routes.append(key)

    routes.append("")
    path = "/".join(routes)

    inferred_req, inferred_req_map = infer(target.request_type, sequence)
    sequence.add_data(inferred_req_map)

    inferred_res, inferred_res_map = infer(target.response_type, sequence)
    sequence.add_data(inferred_res_map)

    sequence.calls.append(
        APICall(
            method=target.method,
            path=path,
            request_payload=inferred_req,
            response_expected_data=inferred_res,
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


def generate_all_sequences(graph: CondGraph) -> Dict[API, List[APISequence]]:
    """
    For each API, generate ALL sequences of API calls
    which resolve all dependency(=incoming edge) and ends with the target API
    """

    call_sequences = defaultdict(list)
    for raw_sequence in iter_path(graph):
        path = [vertex.meta for vertex in raw_sequence.vertices]
        target = path[-1]

        sequence = APISequence(calls=[], param_map={}, data_map=defaultdict(list))
        for node in path:
            generate_call(node, sequence)

        for call in sequence.calls:
            call.request_payload = remove_model_prefix(call.request_payload)

        call_sequences[target].append(sequence)

    return call_sequences


def subarrays(arr):
    for length in range(0, len(arr) + 1):
        for subarray in combinations(arr, length):
            yield list(subarray)


def requireify_field(schema, fields: list[str]):
    # TODO
    return schema


def expand(api: API) -> List[API]:
    """
    expand all optional FK fields
    """
    required_creates = [model for model in api.creates if not model.optional]
    optional_creates = [model for model in api.creates if model.optional]

    required_uses = [model for model in api.uses if not model.optional]
    optional_uses = [model for model in api.uses if model.optional]

    expanded = []
    for indeed_creates in subarrays(optional_creates):
        for indeed_uses in subarrays(optional_uses):
            cardinality = len(indeed_creates) + len(indeed_uses)
            response_type = requireify_field(api.response_type, indeed_creates)
            request_type = requireify_field(api.request_type, indeed_uses)

            expanded.append(
                API(
                    method=api.method,
                    path=api.path,
                    cardinality=cardinality,
                    creates=required_creates + indeed_creates,
                    uses=required_uses + indeed_uses,
                    request_type=request_type,
                    response_type=response_type,
                )
            )

    return expanded


def expand_apis(apis: List[API]):
    expanded = []
    for api in apis:
        expanded.extend(expand(api))
    return expanded


def get_sequences(apis):
    expanded_apis = expand(apis)
    graph = build_graph(expanded_apis)
    return generate_all_sequences(graph)
