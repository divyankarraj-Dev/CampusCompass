"""
Safe calculator. The expression is parsed with Python's `ast` module and only
whitelisted nodes are evaluated, so no arbitrary code can run (unlike raw eval).
"""
import ast
import math
import operator
import re

_BIN = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod, ast.Pow: operator.pow}
_UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}
_FUNCS = {"sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan,
          "log": math.log10, "ln": math.log, "abs": abs, "round": round,
          "floor": math.floor, "ceil": math.ceil}
_CONSTS = {"pi": math.pi, "e": math.e}
_WORDS = [(r"\bmultiplied by\b", "*"), (r"\bdivided by\b", "/"), (r"\bto the power of\b", "**"),
          (r"\bpower\b", "**"), (r"\bplus\b", "+"), (r"\bminus\b", "-"), (r"\btimes\b", "*"),
          (r"\bmod\b", "%"), (r"\binto\b", "*")]
_LEAD = r"\b(calculate|calc|compute|solve|evaluate|what is|what's|math)\b"


def _eval(node):
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _BIN:
        left, right = _eval(node.left), _eval(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 1000:
            raise ValueError("exponent too large")
        return _BIN[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY:
        return _UNARY[type(node.op)](_eval(node.operand))
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in _FUNCS:
        return _FUNCS[node.func.id](*[_eval(a) for a in node.args])
    if isinstance(node, ast.Name) and node.id in _CONSTS:
        return _CONSTS[node.id]
    raise ValueError("unsupported expression")


def calculate(query):
    text = query.lower()
    for pattern, symbol in _WORDS:
        text = re.sub(pattern, symbol, text)
    text = re.sub(_LEAD, "", text).replace("^", "**").strip(" ?=")
    if not text:
        return "Give me an expression, e.g. 'calculate 25 * 4 + 10'."
    try:
        value = _eval(ast.parse(text, mode="eval"))
    except ZeroDivisionError:
        return "Division by zero is undefined."
    except (ValueError, SyntaxError, TypeError):
        return "I could not understand that expression. Try 'calculate 12 * (3 + 4)'."
    if isinstance(value, float):
        value = int(value) if value.is_integer() else round(value, 6)
    return f"{text} = {value}"
