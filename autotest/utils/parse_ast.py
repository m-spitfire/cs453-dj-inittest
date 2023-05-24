import ast
import sys

file = sys.argv[1]
with open(file, "r") as f:
    cont = f.read()

print(ast.dump(ast.parse(cont), indent=4))
