import typing as t

import ast
import json
import argparse
import os
from copy import deepcopy
from pprint import pprint
from dataclasses import dataclass

# from scalpel.import_graph.import_graph import Tree, ImportGraph
from scalpel.call_graph.pycg import CallGraphGenerator

@dataclass
class Serializer:
    name: str
    f_path: str
    model: str
    fields: list[str] | str


@dataclass
class Model:
    name: str
    fields: dict[str, str]
    depends: list[str]

@dataclass
class APINode:
    method: str
    path: str
    request_payload: dict[str,str]
    uses: list[str]
    creates: list[str]

def find_modpath(path: str) -> str:
    """
    converts modpath to file path, assumes last mod is a python file

    path: config.settings
    returns: config/settings.py
    """
    return "/".join(path.split(".")) + ".py"


def parse_file(path: str) -> ast.Module:
    """
    util for reading file and parsing it to ast
    """
    with open(path, "r") as f:
        cont = f.read()
    return ast.parse(cont)


def find_f_call(stmts: list[ast.stmt], fun_name: str) -> ast.Call | None:
    """
    find function call with name `fun_name` among list of statements

    returns: ast.Call object if found, None if not
    """
    for stmt in stmts:
        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
            match type(stmt.value.func):
                case ast.Attribute:
                    # assert type(stmt.value.func) == ast.Attribute
                    if stmt.value.func.attr == fun_name:
                        return stmt.value
                case ast.Name:
                    if stmt.value.func.id == fun_name:
                        return stmt.value
    return None


def find_main(manage_py_path: str) -> ast.FunctionDef:
    """
    find function def named main in manage.py
    """
    with open(manage_py_path, "r") as m_py_f:
        cont = m_py_f.read()
    root = ast.parse(cont)
    for node in ast.walk(root):
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            return node
    raise Exception("manage.py should have main function")


def find_settings(manage_py_path) -> str:
    """
    find settings.py file by analyzing manage.py main func

    returns: settings modpath (e.g. config.settings)
    """
    # Django defines settings module with os.environ.setdefault
    main_f = find_main(manage_py_path)
    env_call = find_f_call(main_f.body, "setdefault")
    if not env_call:
        raise Exception("manage.py should have setdefault call")
    assert (
        type(env_call.args[1]) == ast.Constant
    ), "second argument of setdefault must be constant"
    return env_call.args[1].value


class UrlConfFind(ast.NodeVisitor):
    def __init__(self):
        self.urlconf = None

    def visit_Assign(self, node: ast.Assign):
        # assert isinstance(node.targets[0], ast.Name)
        if (
            isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == "ROOT_URLCONF"
        ):
            assert isinstance(node.value, ast.Constant)
            self.urlconf = node.value.value


def find_urlconf(manage_py_path: str) -> str:
    """
    find urlconf file by analyzing settings file

    returns: urlconf path
    """
    settings_mod = find_settings(manage_py_path)
    settings_mod_path = find_modpath(settings_mod)
    settings_ast = parse_file(settings_mod_path)
    visitor = UrlConfFind()
    visitor.visit(settings_ast)
    return visitor.urlconf

class AppsFinder(ast.NodeVisitor):
    def __init__(self) -> None:
        self.apps: list[str] = []

    def visit_Assign(self, node: ast.Assign):
        if isinstance(node.targets[0], ast.Name) and node.targets[0].id == "INSTALLED_APPS":
            assert isinstance(node.value, ast.List)
            for elem in node.value.elts:
                if isinstance(elem, ast.Constant) and isinstance(elem.value, str) and (not elem.value.startswith("django") or not elem.value.startswith("rest_framework")):
                    self.apps.append(elem.value)


def find_apps(manage_py_path: str) -> list[str]:
    settings_mod = find_settings(manage_py_path)
    settings_mod_path = find_modpath(settings_mod)
    settings_ast = parse_file(settings_mod_path)
    visitor = AppsFinder()
    visitor.visit(settings_ast)
    return visitor.apps


def split_attribute(attr: ast.Attribute) -> list[str]:
    """
    converts a.b.c.as_view to [a,b,c]
    """
    res: list[str] = []
    cur = deepcopy(attr)
    while True:
        if isinstance(cur.value, ast.Name):
            if cur.attr != "as_view":
                res.append(cur.attr)
            res.append(cur.value.id)
            break
        elif isinstance(cur.value, ast.Attribute):
            if cur.attr != "as_view":
                res.append(cur.attr)
            cur = cur.value
        else:
            raise Exception("not supported")
    res.reverse()
    return res


class ImportFinder(ast.NodeVisitor):
    """
    helper for find_view_file
    """

    def __init__(self, id: str):
        self.id = id
        self.import_stmt: ast.ImportFrom | ast.Import | None = None

    def visit_Import(self, node: ast.Import):
        for name in node.names:
            if name.asname is not None and name.asname == self.id:
                self.import_stmt = node
            elif name.name == self.id:
                self.import_stmt = node

    def visit_ImportFrom(self, node: ast.ImportFrom):
        for name in node.names:
            if name.asname is not None and name.asname == self.id:
                self.import_stmt = node
            elif name.name == self.id:
                self.import_stmt = node


def find_view_file(urlconf_root: ast.Module, view_func: ast.Call) -> tuple[str, str]:
    """
    finds where the view func is imported from by analyzing urlconf file

    returns
    tuple[0]: path of view class
    tuple[1]: class name
    """
    # TODO: cover case when view module imported without as
    # e.g from users import views

    assert isinstance(view_func.func, ast.Attribute)
    assert view_func.func.attr == "as_view"
    class_path = split_attribute(view_func.func)
    imp_finder = ImportFinder(class_path[0])
    imp_finder.visit(urlconf_root)
    imp = imp_finder.import_stmt
    path: tuple[str, str]

    # TODO: use os.path.join
    match type(imp):
        case ast.ImportFrom:
            assert type(imp) == ast.ImportFrom
            assert imp.module is not None
            mod_path = "/".join(imp.module.split("."))
            if len(class_path) == 1:
                # class is directly imported
                path = (f"{mod_path}.py", class_path[0])
            else:
                assert len(imp.names) == 1
                path = (f"{mod_path}/{imp.names[0].name}.py", class_path[-1])
        case ast.Import:
            assert type(imp) == ast.Import
            # app is only imported
            assert len(imp.names) == 1
            assert imp.names[0].asname is None
            path = ("{}.py".format("/".join(class_path[:-1])), class_path[-1])
        case None:
            raise Exception("class not found")
    return path


def find_urlpatterns(urlconf_f: str) -> dict[str, tuple[str, str]]:
    """
    Finds url paths to APIView class relation from urlconf file
    """
    root = parse_file(urlconf_f)
    url_to_classpath: dict[str, tuple[str, str]] = {}
    for stmt in root.body:
        if (
            isinstance(stmt, ast.Assign)
            and isinstance(stmt.targets[0], ast.Name)
            and stmt.targets[0].id == "urlpatterns"
        ):
            assert isinstance(stmt.value, ast.List)
            for pattern in stmt.value.elts:
                assert isinstance(pattern, ast.Call)
                assert isinstance(pattern.args[0], ast.Constant) and isinstance(
                    pattern.args[0].value, str
                )
                if "admin" not in pattern.args[0].value:
                    view_func = pattern.args[1]
                    assert isinstance(view_func, ast.Call)
                    url_to_classpath[pattern.args[0].value] = find_view_file(
                        root, view_func
                    )
    return url_to_classpath


class MethodFinder(ast.NodeVisitor):
    """
    Find all the endpoint methods in a APIView class
    """

    def __init__(self, class_name: str):
        self.class_name = class_name
        self.view_funcs: list[ast.FunctionDef] = []
        self.valid_m_names = ["get", "post", "put", "patch", "delete"]

    def visit_ClassDef(self, node: ast.ClassDef):
        if node.name == self.class_name:
            for f_def in node.body:
                if (
                    isinstance(f_def, ast.FunctionDef)
                    and f_def.name in self.valid_m_names
                ):
                    self.view_funcs.append(deepcopy(f_def))


def impfrom_to_path(node: ast.ImportFrom, root_pkg: str):
    """
    convert ast.ImportFrom object to file path

    assumes the importion is not from __init__.py
    """
    level_to_up = "/.." * (node.level - 1)
    assert node.module is not None
    if "." in node.module:
        modpath = "/".join(node.module.split("."))
        if node.level > 0:
            return f"{root_pkg}{level_to_up}/{modpath}.py"
        else:
            return f"{modpath}.py"
    else:
        modpath = node.module
        return f"{root_pkg}{level_to_up}/{modpath}.py"




class ModelInfoExtractor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.models: dict[str, Model] = {}

    @staticmethod
    def get_model_info(node: ast.ClassDef):
        fields = {}
        depends = []
        for stmt in node.body:
            match stmt:
                case ast.Assign(targets=[ast.Name(id=field_name)], value=field_type):
                    assert type(field_type) == ast.Call
                    match field_type:
                        case ast.Call(
                            func=ast.Attribute(value=_, attr=ty),
                            args=[*args],
                            keywords=[*keywords],
                        ):
                            match ty:
                                case "CharField":
                                    fields[field_name] = "text"
                                case "TextField":
                                    fields[field_name] = "text"
                                case "ForeignKey":
                                    assert isinstance(args[0], ast.Name)
                                    fields[f"{args[0].id}::{field_name}"] = "int"
                                    depends.append(args[0].id)
        return {"fields": fields, "depends": depends}


    def visit_ClassDef(self, node):
        for base in node.bases:
            match type(base):
                case ast.Attribute:
                    if base.attr == "Model":
                        mod_info = self.get_model_info(node)
                        self.models[node.name] = Model(node.name, mod_info["fields"], mod_info["depends"])
                        self.generic_visit(node)
                        return
                case ast.Name:
                    if base.id == "Model":
                        mod_info = self.get_model_info(node)
                        self.models[node.name] = Model(node.name, mod_info["fields"], mod_info["depends"])
                        self.generic_visit(node)
                        return


class SerInfoExtractor(ast.NodeVisitor):
    """
    extract serializer information from ser class def
    """

    def __init__(self, class_name: str):
        self.is_serializer = False
        self.ser_info: dict | None = None
        self.class_name = class_name

    @staticmethod
    def get_model_info(node: ast.ClassDef):
        pass

    @staticmethod
    def get_ser_info(node: ast.ClassDef):
        model = None
        fields: str | list[str] | None = None
        for stmt in node.body:
            if isinstance(stmt, ast.ClassDef) and stmt.name == "Meta":
                for meta_stmt in stmt.body:
                    match meta_stmt:
                        case ast.Assign(targets=[ast.Name(id="model")], value=x):
                            assert isinstance(x, ast.Name)
                            model = x.id
                        case ast.Assign(targets=[ast.Name(id="fields")], value=x):
                            match x:
                                case ast.Constant("__all__"):
                                    fields = "__all__"
                                case ast.Tuple(elts):
                                    assert all(
                                        [isinstance(x, ast.Constant) for x in elts]
                                    )
                                    fields = [x.value for x in elts]  # type: ignore

        return {"model": model, "fields": fields}

    def visit_ClassDef(self, node: ast.ClassDef):
        if node.name == self.class_name:
            for base in node.bases:
                match type(base):
                    case ast.Attribute:
                        if base.attr == "ModelSerializer":
                            self.ser_info = self.get_ser_info(node)
                            self.is_serializer = True
                            self.generic_visit(node)
                            return
                    case ast.Name:
                        if base.id == "ModelSerializer":
                            self.ser_info = self.get_ser_info(node)
                            self.is_serializer = True
                            self.generic_visit(node)
                            return


# class ModelFinder(ast.NodeVisitor):
#     """
#     Find currently imported serializers
#     """
#
#     def __init__(self, root_pkg: str):
#         self.models: dict[str, Model] = {}
#         self.root_pkg = root_pkg
#
#     def visit_ImportFrom(self, node: ast.ImportFrom):
#         if node.module and (
#             node.module.startswith("django") or node.module.startswith("rest_framework")
#         ):
#             return
#         f_path = impfrom_to_path(node, self.root_pkg)
#         imported_file = parse_file(f_path)
#         for name in node.names:
#             extractor = ModelInfoExtractor(name.name)
#             extractor.visit(imported_file)
#             if extractor.is_model and extractor.mod_info:
#                 mod_name = name.asname if name.asname else name.name
#                 self.models[mod_name] = Model(mod_name, extractor.mod_info["fields"], extractor.mod_info["depends"])


class SerializerFinder(ast.NodeVisitor):
    """
    Find currently imported serializers
    """

    def __init__(self, root_pkg: str):
        self.serializers: dict[str, Serializer] = {}
        self.root_pkg = root_pkg

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module and (
            node.module.startswith("django") or node.module.startswith("rest_framework")
        ):
            return
        f_path = impfrom_to_path(node, self.root_pkg)
        imported_file = parse_file(f_path)
        for name in node.names:
            extractor = SerInfoExtractor(name.name)
            extractor.visit(imported_file)
            if extractor.is_serializer and extractor.ser_info:
                ser_name = name.asname if name.asname else name.name
                self.serializers[ser_name] = Serializer(
                    ser_name,
                    f_path,
                    extractor.ser_info["model"],
                    extractor.ser_info["fields"],
                )


class ExtractSerializerCall(ast.NodeVisitor):
    def __init__(self, ser_names: list[str]):
        self.ser_call: ast.Call | None = None
        self.ser_names = ser_names
        # self.ser_names = [x.name for x in ser_names]

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in self.ser_names:
            self.ser_call = deepcopy(node)
        self.generic_visit(node)




class ApiExtractor:
    def __init__(self, models: dict[str, Model]) -> None:
        self.serializers: dict[str, dict[str, Serializer]] = {}
        self.models = models
        self.endpoints: list[APINode] = []

    def extract_endpoint(self, url: str, file_name: str, class_name: str):
        """
        extracts all endpoints for a url

        file_name: absolute path to view class
        class_name: view class name
        """
        root = parse_file(file_name)
        root_pkg = "/".join(file_name.split("/")[:-1])
        if file_name not in self.serializers:
            self.extract_serializers(root, file_name, root_pkg)
        serializers = self.serializers[file_name]
        method_finder = MethodFinder(class_name)
        method_finder.visit(root)
        for view in method_finder.view_funcs:
            req_payload_required = False
            creates = False
            ex_ser_obj = ExtractSerializerCall(list(serializers.keys()))
            ex_ser_obj.visit(view)
            ser_call = ex_ser_obj.ser_call
            if ser_call:
                assert isinstance(ser_call.func, ast.Name)
                serializer = serializers[ser_call.func.id]
                req_payload = {}
                if len(ser_call.keywords) > 0 and ser_call.keywords[0].arg == "data":
                    # TODO(important): filter through seralizer fields
                    req_payload = self.models[serializer.model].fields
                    if len(ser_call.args) == 0:
                        creates = True
                if creates:
                    creates_list = [serializer.model]
                    uses_list = self.models[serializer.model].depends
                else:
                    creates_list = []
                    uses_list = [serializer.model]

                self.endpoints.append(
                    APINode(
                        view.name.upper(),
                        url,
                        req_payload,
                        uses_list,
                        creates_list,
                    )
                )
            else:
                # it's an DELETE endpoint (i hope)
                assert view.name == "delete"
                cg_generator = CallGraphGenerator([file_name], root_pkg)
                cg_generator.analyze()
                edges = cg_generator.output_edges()
                edges_map: dict[str, list[str]] = {}
                for caller, callee in edges:
                    edges_map.setdefault(caller,[]).append(callee)
                base_name = os.path.splitext(os.path.basename(file_name))[0]
                func_path = f"{base_name}.{class_name}.{view.name}"
                print(edges_map)
                uses_list = [self.find_rel_model(edges_map, list(self.models.keys()), func_path)]

                self.endpoints.append(
                    APINode(view.name.upper(), url, {}, uses_list, [])
                )

    @staticmethod
    def find_rel_model(cg: dict[str, list[str]], models: list[str], func_path: str) -> str:
        for callee in cg[func_path]:
            model = [x for x in models if f"{x}." in callee]
            if model:
                return model[0]
            else:
                if callee in cg:
                    return ApiExtractor.find_rel_model(cg, models, callee)
                else:
                    pass
        # TODO: LOLOOOLOLOLOL
        # pycg can't detect that User.objects.get is being called
        # sad
        return "User"



    def extract_serializers(self, root: ast.Module, file_name: str, root_pkg: str):
        """
        extract imported serializers from `file_name`
        """
        ser_fder = SerializerFinder(root_pkg)
        ser_fder.visit(root)
        self.serializers[file_name] = ser_fder.serializers

def find_models(app: str) -> dict[str, Model]:
    modelspy_path = os.path.join(app, "models.py")

    if not os.path.exists(modelspy_path):
        return {}

    modelspy_ast = parse_file(modelspy_path)
    info_extr = ModelInfoExtractor()
    info_extr.visit(modelspy_ast)
    return info_extr.models

def main(manage_py_path: str) -> None:
    """Entry"""
    urlconf = find_urlconf(manage_py_path)
    url_to_classpaths = find_urlpatterns(find_modpath(urlconf))
    apps = find_apps(manage_py_path)

    models = {}
    for app in apps:
        models.update(find_models(app))
    # django user
    models["User"] = Model("User", {"username": "text", "email": "email"}, [])
    extractor = ApiExtractor(models)
    for url, cp in url_to_classpaths.items():
        extractor.extract_endpoint(url, cp[0], cp[1])

    pprint(extractor.endpoints)

    # construct_import_graph("posts")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="API Extractor")
    parser.add_argument("manage_py_path")
    args = parser.parse_args()
    main(args.manage_py_path)
