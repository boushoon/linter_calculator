import pytest

from src.calculator import tokenize, infix_to_rpn, evaluate_rpn, calculate


# Тесты для tokenize
@pytest.mark.parametrize("expr, expected_tokens", [
    ("1+2", ["1", "+", "2"]),
    (" 3 + 4 * (2 -1) ", ["3", "+", "4", "*", "(", "2", "-", "1", ")"]),
    ("12.34/5.6", ["12.34", "/", "5.6"]),
])
def test_tokenize_valid(expr, expected_tokens):
    assert tokenize(expr) == expected_tokens


@pytest.mark.parametrize("expr", [
    "1..2 + 3",  # две точки
    "5 + a",  # буква
    ".",  # только точка
])
def test_tokenize_invalid(expr):
    with pytest.raises(ValueError):
        tokenize(expr)


def test_tokenize_empty():
    assert tokenize("") == []


def test_tokenize_only_spaces():
    assert tokenize("   \t\n") == []


# Тесты для infix_to_rpn
def test_infix_to_rpn_simple():
    tokens = ["3", "+", "4", "*", "2", "/", "(", "1", "-", "5", ")"]
    # Ожидаем: 3 4 2 * 1 5 - / +
    rpn = infix_to_rpn(tokens)
    assert rpn == ["3", "4", "2", "*", "1", "5", "-", "/", "+"]


@pytest.mark.parametrize("tokens", [
    ["(", "1", "+", "2"],  # незакрытая скобка
    ["1", "+", "2", ")"],  # лишняя закрывающая
])
def test_infix_to_rpn_unbalanced(tokens):
    with pytest.raises(ValueError):
        infix_to_rpn(tokens)


def test_infix_to_rpn_left_associative():
    tokens = ["2", "-", "3", "-", "4"]
    assert infix_to_rpn(tokens) == ["2", "3", "-", "4", "-"]


def test_infix_to_rpn_nested_parentheses():
    tokens = ["(", "1", "+", "(", "2", "*", "3", ")", ")", "-", "4"]
    assert infix_to_rpn(tokens) == ["1", "2", "3", "*", "+", "4", "-"]


def test_infix_to_rpn_unexpected_token():
    with pytest.raises(ValueError):
        infix_to_rpn(["1", "foo", "2"])


# Тесты для evaluate_rpn
@pytest.mark.parametrize("rpn, expected", [
    (["3", "4", "+"], 7.0),
    (["10", "2", "/", "3", "*"], 15.0),
    (["5", "1", "2", "+", "4", "*", "+", "3", "-"], 14.0),  # классический пример
])
def test_evaluate_rpn_valid(rpn, expected):
    result = evaluate_rpn(rpn)
    assert pytest.approx(result, rel=1e-9) == expected


def test_evaluate_rpn_div_zero():
    with pytest.raises(ZeroDivisionError):
        evaluate_rpn(["1", "0", "/"])


def test_evaluate_rpn_insufficient_operands():
    with pytest.raises(ValueError):
        evaluate_rpn(["1", "+"])


@pytest.mark.parametrize("rpn_tokens", [
    ["1", "2"],
    ["1", "2", "+", "3"],
])
def test_evaluate_rpn_extra_operands(rpn_tokens):
    with pytest.raises(ValueError):
        evaluate_rpn(rpn_tokens)


# Тесты для calculate
@pytest.mark.parametrize("expr, expected", [
    ("1 + 2", 3.0),
    ("2*3 + 4", 10.0),
    ("(2+3)*4", 20.0),
    ("3 + 4 * 2 / (1 - 5)", 3 + 4 * 2 / (1 - 5)),
])
def test_calculate_valid(expr, expected):
    assert pytest.approx(calculate(expr), rel=1e-9) == expected


@pytest.mark.parametrize("expr", [
    "1 +",  # некорректно
    "(",  # некорректно
    "2 / 0",  # деление на ноль
])
def test_calculate_errors(expr):
    with pytest.raises(Exception):
        calculate(expr)


@pytest.mark.parametrize("expr", ["", "   "])
def test_calculate_empty(expr):
    with pytest.raises(ValueError):
        calculate(expr)


@pytest.mark.parametrize("expr, expected", [
    (".5+1", 1.5),
    ("5.+2", 7.0),
])
def test_calculate_float_variants(expr, expected):
    assert pytest.approx(calculate(expr), rel=1e-9) == expected


@pytest.mark.parametrize("expr, expected", [
    ("((2+3)*((4-1)+2))/5", ((2+3)*((4-1)+2))/1),
])
def test_calculate_nested(expr, expected):
    assert pytest.approx(calculate(expr), rel=1e-9) == expected
