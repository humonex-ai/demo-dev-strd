import pytest

from calculator import calculate


@pytest.mark.parametrize(
    "a,op,b,expected",
    [
        (2, "+", 3, 5),
        (10, "-", 4, 6),
        (6, "*", 7, 42),
        (9, "/", 3, 3.0),
        (-2, "+", -3, -5),
        (0, "*", 100, 0),
    ],
)
def test_basic_ops(a, op, b, expected):
    assert calculate(a, op, b) == expected


def test_division_by_zero_raises():
    with pytest.raises(ValueError, match="division by zero"):
        calculate(1, "/", 0)


def test_invalid_operator_raises():
    with pytest.raises(ValueError, match="invalid operator"):
        calculate(1, "%", 2)


def test_float_division():
    assert calculate(1, "/", 4) == pytest.approx(0.25)
