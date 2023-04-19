import ast
from collections import deque, defaultdict
from typing import List, Dict, DefaultDict
from dataclasses import dataclass

@dataclass
class Field:
    name: str
    ty: str

@dataclass
class Model:
    fields: List[Field]


""""    
# TODO what if we want to reuse dependency of dependency?
- e.g.: author of the post wrote a chat to his own post
```
def helper_create_chat2():
    post = helper_create_post()
    chat = Chat.objects.create(post=post, author=post.author)
    chat.save()
    return chat
```

# TODO what if we want to reuse dependency object for multiple field?
-> assign values, maintain ids of them, reuse them
- e.g.: user mentions himself
```
def helper_create_mentions2():
    user = helper_create_user()
    mention = Mention.objects.create(user=user, mentioned=user)
    mention.save()
    return mention
```
"""


def visit_create(model_name: str, model: Model, func_defs: Dict[str, ast.FunctionDef]):
    model_id = model_name.lower()
    body = []
    keywords = []

    for field in model.fields:        
        if field.ty == "text" or field.ty == "varchar":
            # TODO: set some placeholder according to the type
            keywords.append(ast.keyword(
                arg=field.name,
                value=ast.Constant(value='text') 
            ))
        else:
            keywords.append(ast.keyword(
                arg=field.name,
                value=ast.Call(func=ast.Name(id=f'helper_create_{field.ty.lower()}', ctx=ast.Load()), args=[], keywords=[])
            ))

    body.append(ast.Assign(targets=[
        ast.Name(id=model_id, ctx=ast.Store())
    ], value=
        ast.Call(
            func=ast.Attribute(
                value=ast.Attribute(
                    value=ast.Name(id=model_name, ctx=ast.Load()),
                    attr='objects',
                    ctx=ast.Load()
                ),
                attr='create',
                ctx=ast.Load()),
            args=[],
            keywords=keywords
        )
    ))

    body.append(ast.Expr(
                    value=ast.Call(
                        func=ast.Attribute(
                            value=ast.Name(id=model_id, ctx=ast.Load()),
                            attr='save',
                            ctx=ast.Load()),
                        args=[],
                        keywords=[])))
    

    body.append(ast.Return(value=ast.Name(id=model_id, ctx=ast.Load())))

    # define the function to create object of model
    func_defs[model_name] = ast.FunctionDef(
        name=f"helper_create_{model_id}",
        args=[], 
        body=body, 
        decorator_list=[])

def topological_sort(nodes: Dict[str, object], deps: DefaultDict[str, list[str]], visit, acc):
    """
    visits all nodes following:
    - visits all dependencies of a node
    - and then visit the node
    """
    queue = deque()

    # deps[node2] = [node1] : node2 depends on node1 
    # dependers[node1] = [node2] : node2 depends on node1 
    dependers = defaultdict(list)
    in_degrees = defaultdict(int)
    for node in nodes:
        for dep in deps[node]:
            dependers[dep].append(node)
        
        in_degrees[node] = len(deps[node])
        if len(deps[node]) == 0:
            queue.append(node)
    
    while len(queue) > 0:
        node = queue.popleft()
        visit(node, nodes[node], acc)

        # the dependency has been visited 
        for depender in dependers[node]:
            in_degrees[depender] -= 1
            if in_degrees[depender] == 0:
                queue.append(depender)


"""
input: models & dependencies information
output:
"
def helper_create_post():
	u = User.objects.create(...)
	p = Post.objects.create(author=u, title="text")
	return p
"

TODO: handle cycle
- first make object with null field and then nonnull
"""
def make_helper_create(models: Dict[str, Model], deps: DefaultDict[str, List[str]]):
    func_defs = {}
    topological_sort(models, deps, visit_create, func_defs)

    # TODO import all models needed
    root = ast.Module(
        body=list(func_defs.values()), 
        type_ignores=[])
    
    ast.fix_missing_locations(root)
    return ast.unparse(root)


models = {
    "Chat": Model(
        fields=[Field(name="author", ty="User"),
                Field(name="post", ty="Post"),
                Field(name="content", ty="text")]),
    "Post": Model(fields=[Field(name="author", ty="User")]),
    "User": Model(fields=[Field(name="email", ty="varchar")])
}


deps = defaultdict(list)
deps["Post"].append("User")
deps["Chat"] = ["User", "Post"]

print(make_helper_create(models, deps))
