import pytest

from string_calculator.calculator import StringCalculator


@pytest.fixture
def calc():
    return StringCalculator()


def test_empty_string_returns_zero(calc):
    assert calc.add("") == 0


def test_single_number(calc):
    assert calc.add("1") == 1


def test_two_numbers_comma(calc):
    assert calc.add("1,5") == 6

def test_multiple_numbers(calc):
    assert calc.add("1,2,3,4,5") == 15


def test_newlines_are_supported(calc):
    assert calc.add("1\n2,3") == 6


def test_custom_single_char_delimiter(calc):
    assert calc.add("//;\n1;2") == 3

def test_custom_multi_char_delimiter_brackets(calc):
    assert calc.add("//[***]\n1***2***3") == 6

def test_multiple_custom_delimiters(calc):
    assert calc.add("//[*][%]\n1*2%3") == 6
