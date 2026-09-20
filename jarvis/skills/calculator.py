"""A deliberately small, safe arithmetic evaluator for JARVIS."""

from __future__ import annotations

import ast
import operator
import re


_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}
_UNARY_OPERATORS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def calculate(expression: str) -> str:
    """Evaluate basic arithmetic without executing arbitrary Python code."""

    normalized = expression.lower().strip()
    normalized = re.sub(r"\bplus\b", "+", normalized)
    normalized = re.sub(r"\bminus\b", "-", normalized)
    normalized = re.sub(r"\btimes\b", "*", normalized)
    normalized = re.sub(r"\bdivided by\b", "/", normalized)
    normalized = normalized.replace("^", "**")

    try:
        tree = ast.parse(normalized, mode="eval")
        result = _evaluate(tree.body)
    except (ArithmeticError, SyntaxError, ValueError, TypeError, OverflowError):
        return "I can calculate basic arithmetic, but that expression was not valid."

    if isinstance(result, float) and result.is_integer():
        result = int(result)
    return f"The answer is {result}."


def _evaluate(node: ast.AST) -> int | float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        if abs(node.value) > 1_000_000_000:
            raise ValueError("number too large")
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 10:
            raise ValueError("power too large")
        return _BINARY_OPERATORS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
        return _UNARY_OPERATORS[type(node.op)](_evaluate(node.operand))
    raise ValueError("unsupported expression")
