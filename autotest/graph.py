from collections import defaultdict, deque
from typing import List
from interface import APIEdgeInfo, APIGraph, APINode

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


def build_graph(apis: List[APINode]):
    """
    Dependencies between APIs are solely determined by the list of Models
    which the API `creates` and `uses`
    """
    graph = {node: APIEdgeInfo([], []) for node in apis}
    creators = defaultdict(list)
    users = defaultdict(list)

    for node in apis:
        for model in node.creates:
            creators[model].append(node)
        for model in node.uses:
            users[model].append(node)

    # TODO: build multiple graphs from multiple creates
    for model in creators:
        dependency = creators[model][0]
        for depender in users[model]:
            graph[dependency].outgoing.append(depender)
            graph[depender].incoming.append(dependency)

    if has_cycle(graph):
        resolve_cycle(graph)

    return graph


def get_requirements(destination: APINode, graph: APIGraph) -> List[APINode]:
    requirements = []
    queue = deque([destination])

    while queue:
        node = queue.popleft()
        requirements.append(node)
        queue.extend(graph[node].incoming)

    return reversed(requirements)
