from __future__ import annotations

import ast


_ALLOWED_BINOPS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
}


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINOPS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _ALLOWED_BINOPS[type(node.op)](left, right)
    raise ValueError("unsupported expression")


def run(args: dict[str, object]) -> dict[str, object]:
    expression = str(args.get("expression", "")).strip()
    tree = ast.parse(expression, mode="eval")
    result = _eval_node(tree.body)
    return {"result": result}
