import ast
from dataclasses import dataclass
from typing import Any


@dataclass
class APINode:
    method: str
    path: str
    creates: list[str]
    uses: list[str]
    request_type: dict[str, str]
    response_type: dict[str, str]

    def __hash__(self) -> int:
        return hash(self.path) + hash(self.method)


@dataclass
class APICall:
    method: str
    path: str
    request_payload: dict
    response_expected_data: dict


class Generator:
    @classmethod
    def assign(cls, name: str, val: Any) -> ast.Assign:
        return ast.Assign(targets=[ast.Name(id=name, ctx=ast.Store())], value=val)

    @classmethod
    def body_dict(cls, body: dict) -> ast.Dict:
        return ast.Dict(
            keys=[ast.Constant(value=el) for el in body.keys()],
            values=[ast.Constant(value=el) for el in body.values()],
        )

    @classmethod
    def call(cls, method: str, url: str, body: dict) -> ast.Call:
        return ast.Call(
            func=ast.Attribute(
                value=ast.Attribute(
                    value=ast.Name(id="self", ctx=ast.Load()),
                    attr="client",
                    ctx=ast.Load(),
                ),
                attr=method,
                ctx=ast.Load(),
            ),
            args=[ast.Constant(value=url), Generator.body_dict(body)],
            keywords=[],
        )

    @classmethod
    def test_def(cls, testname: str, calls: list[APICall]) -> ast.FunctionDef:
        return ast.FunctionDef(
            name=testname,
            args=ast.arguments(
                posonlyargs=[],
                args=[ast.arg(arg="self")],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[],
            ),
            body=[
                Generator.assign(
                    name=f"res{idx}",
                    val=Generator.call(
                        method=call.method,
                        url=call.path,
                        body=call.request_payload,
                    ),
                )
                for idx, call in enumerate(calls)
            ],
            decorator_list=[],
        )

    @classmethod
    def generate_test(cls, name: str, req: dict[APINode, list[APICall]]) -> ast.Module:
        tests = []
        for node, calls in req.items():
            endpoint = node.path.strip("/").replace("/", "_")
            testname = f"test_{node.method}_{endpoint}"
            tests.append(Generator.test_def(testname, calls))

        res = ast.Module(
            body=[
                ast.ImportFrom(
                    module="django.test", names=[ast.alias(name="TestCase")], level=0
                ),
                ast.ClassDef(
                    name=name,
                    bases=[ast.Name(id="TestCase", ctx=ast.Load())],
                    keywords=[],
                    body=tests,
                    decorator_list=[],
                ),
            ],
            type_ignores=[],
        )

        return ast.fix_missing_locations(res)


def main() -> None:
    req = {
        APINode("get", "/posts/1", [], [], {}, {}): [
            APICall(
                "post",
                "/users",
                {"name": "Shin Yoo", "email": "shin.yoo@kaist.ac.kr"},
                {},
            ),
            APICall(
                "post",
                "/posts",
                {
                    "user_id": 1,
                    "title": "Title of a post",
                    "content": "Lorem Ipsum Dolar",
                },
                {},
            ),
            APICall(
                "get",
                "/posts/1",
                {},
                {},
            ),
        ]
    }

    test_ast = Generator.generate_test("MyTestCase", req)

    with open("generated_test.py", "w") as test_file:
        test_file.write(ast.unparse(test_ast))


if __name__ == "__main__":
    main()
