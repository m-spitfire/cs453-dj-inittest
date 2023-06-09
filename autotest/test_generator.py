import ast
from typing import Any

from interface import API, APICall, APISequence, Method, ResMap, Url


class Generator:
    @classmethod
    def _get_res_node(self, idx: int, values: list[int | str]) -> ast.Subscript:
        res = ast.Attribute(
            value=ast.Name(id=f"res{idx}", ctx=ast.Load()),
            attr="data",
            ctx=ast.Load(),
        )
        for val in values:
            res = ast.Subscript(
                value=res,
                slice=ast.Constant(value=val),
                ctx=ast.Load(),
            )
        return res

    @classmethod
    def _get_url_node(self, raw_url: str, res_map: ResMap) -> Url:
        url_splt = raw_url.strip("/").split("/")
        if not any([el in res_map for el in url_splt]):
            return ast.Constant(value="/" + "/".join(url_splt) + "/")
        values = [ast.Constant(value="/")]
        for el in url_splt:
            if el in res_map:
                values.append(ast.FormattedValue(value=res_map[el], conversion=-1))
                values.append(ast.Constant(value="/"))
            else:
                values.append(ast.Constant(value=f"{el}/"))
        return ast.JoinedStr(values=values)

    @classmethod
    def assign(cls, name: str, val: Any) -> ast.Assign:
        return ast.Assign(targets=[ast.Name(id=name, ctx=ast.Store())], value=val)

    @classmethod
    def body_dict(cls, body: dict[str, Any], res_map: ResMap) -> ast.Dict:
        return ast.Dict(
            keys=[ast.Constant(value=el) for el in body.keys()],
            values=[
                res_map[el] if el in res_map else ast.Constant(value=el)
                for el in body.values()
            ],
        )

    @classmethod
    def call(cls, method: Method, url: Url, body: ast.Dict) -> ast.Call:
        return ast.Call(
            func=ast.Attribute(
                value=ast.Attribute(
                    value=ast.Name(id="self", ctx=ast.Load()),
                    attr="client",
                    ctx=ast.Load(),
                ),
                attr=method.lower(),
                ctx=ast.Load(),
            ),
            args=[url, body, ast.Constant(value="application/json")],
            keywords=[],
        )

    @classmethod
    def gen_test(cls, testname: str, sequence: APISequence) -> ast.FunctionDef:
        res_map: ResMap = {
            key: cls._get_res_node(idx, values)
            for key, (idx, values) in sequence.param_map.items()
        }

        body = []
        for idx, call in enumerate(sequence.calls):
            url = cls._get_url_node(call.path, res_map)
            bdy = cls.body_dict(call.request_payload, res_map)
            val = cls.call(call.method, url, bdy)
            assignment = cls.assign(f"res{idx}", val)
            body.append(assignment)
            body.append(
                ast.Assert(
                    test=ast.Compare(
                        left=ast.Attribute(
                            value=ast.Name(id=f"res{idx}", ctx=ast.Load()),
                            attr="status_code",
                            ctx=ast.Load(),
                        ),
                        ops=[ast.Lt()],
                        comparators=[ast.Constant(value=400)],
                    )
                )
            )

        return ast.FunctionDef(
            name=testname,
            args=ast.arguments(
                posonlyargs=[],
                args=[ast.arg(arg="self")],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[],
            ),
            body=body,
            decorator_list=[],
        )

    @classmethod
    def gen_test_file(
        cls,
        filename: str,
        testcasename: str,
        sequences: dict[API, list[APISequence]],
    ) -> None:
        tests = []
        for target, sequence_list in sequences.items():
            method = target.method.lower()
            endpoint_lst = target.path.strip("/").split("/")
            for seq_idx, sequence in enumerate(sequence_list):
                endpoint = "_".join(
                    [
                        "detail" if el in sequence.param_map or "pk" in el else el
                        for el in endpoint_lst
                    ]
                )
                testname = f"test_{method}_{endpoint}_{seq_idx}"
                # print(testname)
                tests.append(cls.gen_test(testname, sequence))

        res = ast.Module(
            body=[
                ast.ImportFrom(
                    module="django.test",
                    names=[ast.alias(name="TestCase")],
                    level=0,
                ),
                ast.ClassDef(
                    name=testcasename,
                    bases=[ast.Name(id="TestCase", ctx=ast.Load())],
                    keywords=[],
                    body=tests,
                    decorator_list=[],
                ),
            ],
            type_ignores=[],
        )
        res = ast.fix_missing_locations(res)

        with open(filename, "w") as test_file:
            test_file.write(ast.unparse(res))


def main() -> None:
    target1 = APICall(
        "GET",
        "/posts/$1/",
        {},
        {},
    )
    sequence1 = APISequence(
        calls=[
            APICall(
                "POST",
                "uesrs/",
                {"email": "shin.yoo@kaist.ac.kr", "username": "Shin Yoo"},
                {},
            ),
            APICall(
                "POST",
                "posts/",
                {
                    "author": "$0",
                    "title": "Title of a post",
                    "content": "Lorem Ipsum Dolar",
                },
                {},
            ),
            APICall(
                "GET",
                "posts/$1/",
                {},
                {},
            ),
        ],
        param_map={
            "$0": (0, ["id"]),
            "$1": (1, ["id"]),
        },
    )

    target2 = APICall(
        "GET",
        "/posts/",
        {},
        {},
    )
    sequence2 = APISequence(
        calls=[
            APICall(
                "POST",
                "uesrs/",
                {"email": "shin.yoo@kaist.ac.kr", "username": "Shin Yoo"},
                {},
            ),
            APICall(
                "GET",
                "posts/",
                {"author": "$0"},
                {},
            ),
        ],
        param_map={
            "$0": (0, ["id"]),
        },
    )

    sequences = {target1: sequence1, target2: sequence2}

    Generator.gen_test_file("generated_test.py", "MyTestCase", sequences)


if __name__ == "__main__":
    main()
