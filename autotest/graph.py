from collections import defaultdict
from typing import DefaultDict, Dict, List, Set
from interface import API, ConvNode, CondNode, CondGraph, ConvSequence


def build_graph(apis: List[API]):
    """
    Dependencies between APIs are solely determined by the list of Models
    which the API `creates` and `uses`
    """

    cond_nodes: Dict[str, CondNode] = {}
    conv_nodes: Dict[str, ConvNode] = {}

    for api in apis:
        if api.cardinality == 0:
            label = f"{api.method} {api.path}"
        else:
            label = f"{api.method} {api.path}{api.cardinality}"

        if label not in conv_nodes:
            conv_nodes[label] = ConvNode(label=label, meta=api)

        vertex = conv_nodes[label]

        for model in api.creates:
            # assume all expanded
            assert not model.optional

            label = model.name
            if label not in cond_nodes:
                cond_nodes[label] = CondNode(label)

            condition = cond_nodes[label]
            vertex.creates.append(condition)

        for model in api.uses:
            # assume all expanded
            assert not model.optional

            label = model.name
            if label not in cond_nodes:
                cond_nodes[label] = CondNode(label)

            condition = cond_nodes[label]
            vertex.uses.append(condition)

    graph = CondGraph(cond_nodes=cond_nodes, conv_nodes=conv_nodes)
    return graph


def visitable(satisfied_conditions: DefaultDict[CondNode, int], vertex: ConvNode):
    for condition in vertex.uses:
        if satisfied_conditions[condition] == 0:
            return False

    return True


def extending(satisfied_conditions: DefaultDict[CondNode, int], vertex: ConvNode):
    for condition in vertex.creates:
        if satisfied_conditions[condition] == 0:
            return True
    return False


def depends(current_vertex: ConvNode, end_vertex: ConvNode):
    satisfying_conditions = set(current_vertex.creates)
    using_conditions = set(end_vertex.uses)
    return len(satisfying_conditions.intersection(using_conditions)) > 0


def find_paths_to_reach_target(
    target, satisfied_conditions, path, sequences, visited, vertices
):
    if visitable(satisfied_conditions, target):
        sequences.append(ConvSequence(path + [target]))
        return

    """
    find the next vertex to visit
    """
    for vertex in vertices:
        if vertex in visited:
            continue

        if not visitable(satisfied_conditions, vertex):
            continue

        if not depends(vertex, target):
            continue

        for model in vertex.creates:
            satisfied_conditions[model] += 1

        visited.add(vertex)

        find_paths_to_reach_target(
            target, satisfied_conditions, path + [vertex], sequences, visited, vertices
        )

        visited.remove(vertex)

        for model in vertex.creates:
            satisfied_conditions[model] -= 1

    """
    target may be unreachable
    """
    return


def iter_path(graph: CondGraph) -> Set[ConvSequence]:
    """
    generate all possible sequence from graph
    TODO: Add cache
    TODO: refactor with yield to use less memory
    """

    # Assume that no vertex with empty uses & empty creates
    vertices = graph.conv_nodes.values()

    """
    start from vertex with many requirements
    traverse all possible cases 
    """

    sequences: List[ConvSequence] = []

    for target in vertices:
        visited = set()
        path = []
        satisfied_conditions = defaultdict(int)

        find_paths_to_reach_target(
            target, satisfied_conditions, path, sequences, visited, vertices
        )

    return sequences
