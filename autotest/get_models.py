import ast
import pprint
import sys

import constraints
import fieldtype

from node import ModelNode, FieldNode


def check_inh(attr):
    return attr.value.id == "models" and attr.attr == "Model"


def make_generic_constraints(field: FieldNode, stmt: ast.Assign) -> None:
    """It mutates the original field object"""
    nullable = False
    unique = False
    for kw in stmt.value.keywords:
        match kw.arg:
            case "null":  
                # TODO: this works only when constant is passed
                assert isinstance(kw.value, ast.Constant)
                nullable = kw.value.value
            case "unique":
                assert isinstance(kw.value, ast.Constant)
                unique = kw.value.value
    if not nullable:
        field.constraints.add(constraints.NotNull())
    if unique:
        field.constraints.add(constraints.Unique())


class ClassDefVisitor(ast.NodeVisitor):
    """
    extract the model information
    """
    def __init__(self) -> None:
        self.models = set()
    
    def visit_ClassDef(self, node: ast.ClassDef):
        ok = False
        for base in node.bases:
            if check_inh(base):
                # a django model
                ok = True
                break

        if not ok:
            return self.generic_visit(node)
        model = ModelNode(name=node.name)
        # name = node.name
        # self.models[name] = {}
        fields = set()
        for stmt in node.body:
            if isinstance(stmt, ast.Assign) and isinstance(stmt.value, ast.Call):
                # Get field name
                assert len(stmt.targets) == 1
                field_name = stmt.targets[0].id

                match stmt.value.func.attr:
                    case "CharField":
                        field = FieldNode(fieldtype.Varchar(), field_name)
                    
                        for kw in stmt.value.keywords:
                            match kw.arg:
                                case "max_length":  
                                    # TODO: this works only when constant is passed
                                    assert isinstance(kw.value, ast.Constant)
                                    field.type.max_len = kw.value.value
                        make_generic_constraints(field, stmt)
                        fields.add(field)
                    case "TextField":
                        field = FieldNode(fieldtype.Text(), field_name)
                        make_generic_constraints(field, stmt)
                        fields.add(field)
                    case "DateTimeField":
                        if ast.keyword(arg="auto_now_add", value=ast.Constant(value=True)) in stmt.value.keywords:
                            # we don't need to specify datetime if auto_now_add is set to True
                            continue
                    case "ForeignKey":
                        assert len(stmt.value.args) == 1 and isinstance(stmt.value.args[0], ast.Name)
                        fk_model_name = stmt.value.args[0].id
                        field = FieldNode(type=fieldtype.Model, name=fk_model_name)
                        make_generic_constraints(field, stmt)
                        fields.add(field)
        model.fields = fields
        self.models.add(model)


def get_models(app):
    path = app + "/models.py"  # Assuming the project has the Django default directory structure
    with open(path, "r") as f:
        x = f.readlines()
    root = ast.parse("".join(x), path)
    # print(ast.dump(root, indent=4))
    cvisitor = ClassDefVisitor()
    cvisitor.visit(root)
    user_def = ModelNode("User", {FieldNode(fieldtype.Varchar(254), "email", {constraints.NotNull()}), 
                                  FieldNode(fieldtype.Varchar(150), "username", {constraints.NotNull()}),
                                  FieldNode(fieldtype.Varchar(128), "password", {constraints.NotNull()})})
    ms = cvisitor.models
    ms.add(user_def)
    return ms


def main() -> None:
    apps = sys.argv[1:]

    for app in apps:
        pprint.PrettyPrinter(width=41, compact=True).pprint(get_models(app))

if __name__ == '__main__':
    main()
