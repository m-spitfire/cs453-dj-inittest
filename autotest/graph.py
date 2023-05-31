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
        label = f"{api.method} {api.path}"
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


def dfs(
    current_vertex: ConvNode,
    visited: Set[ConvNode],
    path: List[ConvNode],
    valid_paths: List[List[ConvNode]],
    vertices: List[ConvNode],
    satisfied_conditions: DefaultDict[CondNode, int],
    end_vertices: List[ConvNode],
    sequences,
):
    visited.add(current_vertex)
    path.append(current_vertex)

    for model in current_vertex.creates:
        satisfied_conditions[model] += 1

    extended = False

    for vertex in vertices:
        if vertex in visited:
            continue

        if not visitable(satisfied_conditions, vertex):
            continue

        if not extending(satisfied_conditions, vertex):
            continue

        extended = True
        dfs(
            vertex,
            visited,
            path,
            valid_paths,
            vertices,
            satisfied_conditions,
            end_vertices,
            sequences,
        )

    if not extended:
        valid_paths.append(path.copy())

    """
    end vertex에서 reachable한 게 생기면 sequence에 add
    """
    for end_vertex in end_vertices:
        if depends(current_vertex, end_vertex) and visitable(
            satisfied_conditions, end_vertex
        ):
            sequences.add(ConvSequence(calls=path.copy() + [end_vertex]))

    for model in current_vertex.creates:
        satisfied_conditions[model] -= 1

    visited.remove(current_vertex)
    path.pop()


def reduce(vertices: List[ConvNode]):
    if len(vertices) == 1:
        return vertices

    destination = vertices[-1]

    total_uses = set()
    for vertex in vertices:
        for model in vertex.uses:
            total_uses.add(model)

    reduced_vertices = []
    for vertex in vertices:
        if len(total_uses.intersection(set(vertex.creates))) == 0:
            continue

        reduced_vertices.append(vertex)

    reduced_vertices.append(destination)
    return reduced_vertices


def iter_path(graph: CondGraph) -> Set[ConvSequence]:
    """
    generate all possible sequence from graph
    TODO: Add cache
    TODO: refactor with yield to use less memory
    """

    # Assume that no vertex with empty uses & empty creates

    vertices = graph.conv_nodes
    valid_paths = []

    # entry points
    start_vertices = [vertex for vertex in vertices if len(vertex.uses) == 0]

    # use-only apis
    end_vertices = [vertex for vertex in vertices if len(vertex.creates) == 0]

    sequences: Set[ConvSequence] = set()

    for start_vertex in start_vertices:
        visited = set()
        path = []
        satisfied_conditions = defaultdict(int)

        dfs(
            start_vertex,
            visited,
            path,
            valid_paths,
            vertices,
            satisfied_conditions,
            end_vertices,
            sequences,
        )

    for path in valid_paths:
        n = len(path)
        for length in range(1, n + 1):
            subpath = reduce(path[:length])
            if len(subpath) == 0:
                continue
            sequences.add(ConvSequence(vertices=subpath))

    return sequences
