from collections import defaultdict
from dataclasses import dataclass

from .node import FieldNodeType, ModelNode

"""
input: {
	'Post': {'id': 'number', 'author': 'User', ...},
	'User': {...}
}
output: { Post: [User] }
"""


def find_dependencies(models):
    graph = defaultdict(list)
    nodes = models.keys()

    for node in nodes:
        for dep in models[node]:
            if dep in nodes:
                graph[node].append(dep)

    return graph


def find_deps_v2(models: set[ModelNode]):
    graph = defaultdict(set)
    for model in models:
        fk_dep_models = {
            field
            for field in model.fields
            if isinstance(field.type, FieldNodeType.MODEL)
        }
        graph[model.name] = fk_dep_models
    return graph


def test1():
    input = {
        "Post": {"id": "number", "author": "User"},
        "User": {"id": "number"},
    }

    expected = {
        "Post": ["User"],
    }

    output = find_dependencies(input)
    print(output)


def test2():
    input = {
        "Chat": {"id": "number", "reply": "Chat"},
    }

    expected = {
        "Chat": ["Chat"],
    }
