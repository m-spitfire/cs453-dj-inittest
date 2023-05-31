from collections import defaultdict
from pprint import pprint
from typing import Any, DefaultDict, List, Set

class Model:
    def __init__(self, name, optional=False) -> None:
        self.name = name
        self.optional = optional

class Node:
    def __init__(self, label, uses, creates):
        self.label = label
        self.uses = uses
        self.creates = creates

    def __repr__(self) -> str:
        return str(self.label)
    
    def __hash__(self) -> int:
        return hash(str(self.label))
    
    def __eq__(self, __value: object) -> bool:
        return self.label == __value.label
    
class Sequence:
    calls: List[Node]

    def __init__(self, calls) -> None:
        self.calls = calls

    def __hash__(self) -> int:
        # TODO: cyclic API hash
        return hash(str(self))
    
    def __repr__(self) -> str:
        labels = [node.label for node in self.calls]
        return " -> ".join(labels)
    
    def __eq__(self, __value: object) -> bool:
        for my_call in self.calls:
            for their_call in __value.calls:
                if my_call != their_call:
                    return False
        return True


def visitable(created_models: DefaultDict[Any, int], node: Node):
    for model in node.uses:
        if created_models[model] == 0:
            return False

    return True


def expanding(created_models: DefaultDict[Any, int], node: Node):
    for model in node.creates:
        if created_models[model] == 0:
            return True

    return False

def depends(current_node, end_node):
    creating_models = set(current_node.creates)
    using_models = set(end_node.uses)
    return len(creating_models.intersection(using_models)) > 0


def dfs(
    current_node: Node,
    visited: Set[Node],
    path: List[Node],
    valid_paths: List[List[Node]],
    nodes: List[Node],
    created_models: DefaultDict[Any, int],
    end_nodes,
    sequences
):
    visited.add(current_node)
    path.append(current_node)

    for model in current_node.creates:
        created_models[model] += 1

    extended = False

    for node in nodes:
        if node in visited:
            continue

        if not visitable(created_models, node):
            continue

        if not expanding(created_models, node):
            continue

        extended = True
        dfs(node, visited, path, valid_paths, nodes, created_models, end_nodes, sequences)

    if not extended:
        valid_paths.append(path.copy())

    """
    end node에서 reachable한 게 생기면 sequence에 add
    """
    for end_node in end_nodes:
        if depends(current_node, end_node) and visitable(created_models, end_node):
            sequences.add(Sequence(calls=path.copy()+[end_node]))

    for model in current_node.creates:
        created_models[model] -= 1

    visited.remove(current_node)
    path.pop()


def reduce(calls: List[Node]):
    if len(calls) == 1:
        return calls
    
    target = calls[-1]

    total_uses = set()
    for node in calls:
        for model in node.uses:
            total_uses.add(model)
    
    reduced_calls = []
    for node in calls:
        if len(total_uses.intersection(set(node.creates))) == 0:
            continue

        reduced_calls.append(node)

    reduced_calls.append(target)
    return reduced_calls

def getAllPaths(nodes):
    """
    어떤 use도 create도 하지 않는 애들은 없다고 가정
    """

    valid_paths = []
    start_nodes = [node for node in nodes if len(node.uses) == 0]
    end_nodes = [node for node in nodes if len(node.creates) == 0] # use-only apis
    sequences = set()

    for start_node in start_nodes:
        visited = set()
        path = []
        created_models = defaultdict(int)

        """
        dfs의 각 단계마다 현재 생성된 모델 종류는 증가함
        각 단계 뒤에 붙일 수 있는 end_node 구하자
        
        subpath를 구하는건 create sequence만이고, 끝에 use-only API 붙어있는 sequence는 굳이 subpath를 다시 계산할 필요가 없음
        """
        dfs(start_node, visited, path, valid_paths, nodes, created_models, end_nodes, sequences)
    
    for path in valid_paths:
        n = len(path)
        for length in range(1, n+1):
            subpath = reduce(path[:length])
            if len(subpath) == 0:
                continue
            sequences.add(Sequence(calls=subpath))

    return sequences


nodes = [
    Node("POST /users", uses=[], creates=["User"]),
    Node("GET /users", uses=["User"], creates=[]),
    Node("POST /posts", uses=["User"], creates=["Post"]),
    Node("POST /fancy-posts", uses=["User"], creates=["Post"]),
    Node("POST /comments", uses=["Post"], creates=["Comment"]),
    Node("GET /comments", uses=["Comment"], creates=[]),
    Node("GET /posts", uses=["Post"], creates=[]),
]

pprint(getAllPaths(nodes))

