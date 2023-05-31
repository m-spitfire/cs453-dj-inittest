import ast
from collections import defaultdict, deque
from typing import DefaultDict, Deque, List
from interface import APIEdgeInfo, APIGraph, API


def build_graph(apis: list[API]):
    """
    Dependencies between APIs are solely determined by the list of Models
    which the API `creates` and `uses`
    """
    creators = defaultdict(list)
    users = defaultdict(list)

    for node in apis:
        for model in node.creates:
            creators[model].append(node)
        for model in node.uses:
            users[model].append(node)

    graph = APIGraph(creators, users)
    return graph

def iter_path(nodes: List[API]) -> List[API]:
    """
    generate all possible path from graph
    TODO: Add cache
    
    일단 uses가 없는 것부터 deque에 넣는다

    TODO: check cycle
    현재 target이 optional 필드를 만족시키기 위해서는 cycle이 필요한지 확인
    이후 cycle 을 해소할 수 있도록 중복 path를 먼저 방문
    TODO: resolve cycle

    ast.walk 참고
    """
    users: DefaultDict[str, List[API]] = defaultdict(list)
    creators: DefaultDict[str, List[API]] = defaultdict(list)



    def helper(src: API, dest: API, path: List[API], model_counter, visited):
        if src == dest:
            yield path
            return
        
        children = set()

        for model in src.creates:
            # TODO: update model counter
            # TODO: get visitable nodes
            set(users[model])

        children.difference_update(visited)

        for node in children:
            path.append(node)
            helper(node, dest, path, model_counter, visited)
            path.pop()

        # push the source node in the path

        

    model_counter = defaultdict(int)
    cur_path = []
    
    for path in helper(model_counter, cur_path):
        yield path
