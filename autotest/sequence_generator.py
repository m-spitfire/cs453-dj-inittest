"""
Generate sequences that ends with each and every API call
"""
from collections import defaultdict
from copy import deepcopy
from typing import List, Dict
from graph import build_graph, iter_path
from infer import infer, infer_id
from interface import APICall, APISequence, API, CondGraph, Model
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

    variable starts with '$'
    can be retrieved from data_map in sequence
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
        key = infer_id("id", model_name, sequence)
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
    paths = iter_path(graph)
    print(f"total sequences: {len(paths)}")
    for raw_sequence in paths:
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


def filter_fields(fields: list[str], models: list[str]):
    return [
        field for field in fields if any([field.startswith(model) for model in models])
    ]


def requireify_fields(schema, models: list[str]):
    if len(schema) == 0:
        return schema
    schema = deepcopy(schema)

    if schema["type"] == "object":
        fields = filter_fields(schema["properties"].keys(), models)
        schema["required"].extend(fields)

        keys = list(schema["properties"].keys())

        for property in keys:
            if "::" in property and property not in schema["required"]:
                del schema["properties"][property]

    if schema["type"] == "array":
        fields = filter_fields(schema["items"]["properties"].keys(), models)
        schema["items"]["required"].extend(fields)

        keys = list(schema["items"]["properties"].keys())

        for property in keys:
            if "::" in property and property not in schema["items"]["required"]:
                del schema["items"]["properties"][property]

    return schema


def expand(api: API) -> List[API]:
    """
    expand all optional FK fields
    """
    required_creates = [model.name for model in api.creates if not model.optional]
    optional_creates = [model.name for model in api.creates if model.optional]

    required_uses = [model.name for model in api.uses if not model.optional]
    optional_uses = [model.name for model in api.uses if model.optional]

    expanded = []
    for indeed_creates in subarrays(optional_creates):
        for indeed_uses in subarrays(optional_uses):
            cardinality = len(indeed_creates) + len(
                indeed_uses
            )  # TODO: cardinality may not be unique
            response_type = requireify_fields(api.response_type, indeed_creates)
            request_type = requireify_fields(api.request_type, indeed_uses)

            expanded.append(
                API(
                    method=api.method,
                    path=api.path,
                    cardinality=cardinality,
                    creates=[Model(name) for name in required_creates + indeed_creates],
                    uses=[Model(name) for name in required_uses + indeed_uses],
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
    expanded_apis = expand_apis(apis)
    graph = build_graph(expanded_apis)
    return generate_all_sequences(graph)
