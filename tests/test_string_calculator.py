import pytest

from string_calculator.calculator import StringCalculator


@pytest.fixture
def calc():
    return StringCalculator()


def test_empty_string_returns_zero(calc):
    assert calc.add("") == 0


def test_single_number(calc):
    assert calc.add("1") == 1
