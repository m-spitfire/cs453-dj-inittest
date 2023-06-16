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


def is_condition_met(required_conditions):
    for cond in required_conditions:
        if required_conditions[cond] > 0:
            return False

    return True


def is_relevant_vertex(required_conditions, vertex):
    for cond in required_conditions:
        if required_conditions[cond] > 0 and cond in vertex.creates:
            return True

    return False


def satisfy(satisfied_conditions, required_conditions, vertex):
    for model in vertex.creates:
        satisfied_conditions[model] += 1

        if model in required_conditions:
            required_conditions[model] -= 1


def unsatisfy(satisfied_conditions, required_conditions, vertex):
    for model in vertex.creates:
        satisfied_conditions[model] -= 1

    if model in required_conditions:
        required_conditions[model] += 1


def find_paths_to_reach_target(
    target,
    required_conditions,
    satisfied_conditions,
    path,
    all_paths,
    visited,
    vertices,
):
    if is_condition_met(required_conditions):
        all_paths.append(path + [target])
        return

    """
    find the next vertex to visit
    """
    for vertex in vertices:
        if vertex in visited:
            continue

        if not is_relevant_vertex(required_conditions, vertex):
            continue

        all_paths_to_visit_vertex = []
        satisfied_conditions_to_visit_vertex = satisfied_conditions.copy()
        visited_to_visit_vertex = visited.copy()
        path_to_visit_vertex = []

        find_paths_to_reach_target(
            vertex,
            vertex_requirements(vertex),
            satisfied_conditions_to_visit_vertex,
            path_to_visit_vertex,
            all_paths_to_visit_vertex,
            visited_to_visit_vertex,
            [v for v in vertices if v is not vertex],
        )

        original_visited = visited.copy()
        for p in all_paths_to_visit_vertex:
            for v in p:
                satisfy(satisfied_conditions, required_conditions, v)
                visited.add(v)
            find_paths_to_reach_target(
                target,
                required_conditions,
                satisfied_conditions,
                path + p,
                all_paths,
                visited,
                vertices,
            )
            for v in p:
                visited.remove(v)
                unsatisfy(satisfied_conditions, required_conditions, v)
            assert (
                len(visited)
                == len(original_visited)
                == len(visited.intersection(original_visited))
            )

    return


def vertex_requirements(vertex):
    required_conditions = defaultdict(int)

    for cond in vertex.uses:
        required_conditions[cond] += 1

    return required_conditions


def iter_path(graph: CondGraph) -> Set[ConvSequence]:
    """
    generate all possible sequence from graph
    TODO: Add cache
    TODO: refactor with yield to use less memory
    """

    # Assume that no vertex with empty uses & empty creates
    vertices = list(graph.conv_nodes.values())

    """
    start from vertex with no requirement
    traverse all possible cases 
    """

    vertices.sort(key=lambda v: len(v.uses))
    sequences: List[ConvSequence] = []

    for target in vertices:
        visited = set()
        path = []
        all_paths = []
        required_conditions = vertex_requirements(target)
        satisfied_conditions = defaultdict(int)

        find_paths_to_reach_target(
            target,
            required_conditions,
            satisfied_conditions,
            path,
            all_paths,
            visited,
            [v for v in vertices if v is not target],
        )

        for path in all_paths:
            sequences.append(ConvSequence(vertices=path))

    return sequences
