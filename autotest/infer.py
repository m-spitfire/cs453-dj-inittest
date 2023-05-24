from collections import defaultdict
from jsf import JSF

from interface import APISequence
from utils import get_cleaned_key, get_model_name


def infer_id(model_name: str, sequence: APISequence) -> str:
    """
    response type 중 model_name에 해당하는 model의 key를 값으로 하는
    field가 있으면 해당 값 사용
    """

    def find(obj, criteria, access_trace):
        if type(obj) == list:
            for i, e in enumerate(obj):
                if find(e, criteria, access_trace):
                    access_trace.append(i)
                    return True

        if type(obj) == dict:
            for key in obj:
                if criteria(key):
                    access_trace.append(get_cleaned_key(key))
                    return True

                if find(obj[key], criteria, access_trace):
                    access_trace.append(key)
                    return True

        return False

    n = len(sequence.calls)

    for i, call in enumerate(reversed(sequence.calls)):
        access_trace = []
        find(
            call.response_expected_data,
            lambda key: key.startswith(model_name),
            access_trace,
        )

        if len(access_trace) > 0:
            value = list(reversed(access_trace))

            return sequence.add_param((n - 1 - i, value))

    return sequence.add_param(0)


def fake(object) -> dict:
    faker = JSF(object)
    return faker.generate()


def infer(schema: dict, sequence: APISequence):
    infer_map = defaultdict(list)

    def fill_prev_data(faked):
        def get_new_value(key, value):
            if isinstance(value, dict) or isinstance(value, list):
                return helper(value)

            if len(sequence.data_map[key]) == 0:
                infer_map[key].append(value)
                return value

            inferred_value = sequence.data_map[key][0]
            infer_map[key].append(inferred_value)
            return inferred_value

        def helper(original):
            if isinstance(original, dict):
                new_items = []
                for key, value in original.items():
                    new_value = get_new_value(key, value)
                    new_items.append((key, new_value))
                return dict(new_items)

            elif isinstance(original, list):
                new_values = []
                for item in original:
                    new_value = helper(item)
                    new_values.append(new_value)
                return new_values

            return original

        return helper(faked)

    def replace_model_id(filled):
        """
        filled를 traverse하면서 key가 model_name이면 해당 key의 value를 infer_id의 결과값으로 replace
        """
        if isinstance(filled, dict):
            new_items = []
            for key, value in filled.items():
                model_name = get_model_name(key)
                new_value = (
                    replace_model_id(value)
                    if model_name is None
                    else infer_id(model_name, sequence)
                )
                new_items.append((key, new_value))
            return dict(new_items)

        elif isinstance(filled, list):
            new_values = []
            for item in filled:
                new_value = replace_model_id(item)
                new_values.append(new_value)
            return new_values

        return filled

    if len(schema) == 0:
        return {}, defaultdict(list)

    faked = fake(schema)
    filled = fill_prev_data(faked)
    replaced = replace_model_id(filled)

    return replaced, infer_map
