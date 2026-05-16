from __future__ import annotations

import sys

_OPS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
}


def calculate(a: float, op: str, b: float) -> float:
    if op not in _OPS:
        raise ValueError(f"invalid operator: {op!r}; expected one of {sorted(_OPS)}")
    if op == "/" and b == 0:
        raise ValueError("division by zero")
    return _OPS[op](a, b)


def _main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: python calculator.py <a> <op> <b>", file=sys.stderr)
        return 2
    a_str, op, b_str = argv
    try:
        a = float(a_str)
        b = float(b_str)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    try:
        result = calculate(a, op, b)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv[1:]))
