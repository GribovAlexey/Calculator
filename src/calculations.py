import re
from decimal import Decimal, ROUND_HALF_UP

OPERATORS = {"+": (1, lambda a, b: a + b), "-": (1, lambda a, b: a - b),
             "*": (2, lambda a, b: a * b), "/": (2, lambda a, b: a / b)}
BRACKETS = "()"
NUMS = "1234567890."
ACCEPTABLE = [*NUMS, *BRACKETS, *OPERATORS, " "]


def math_round(num, sign_count=3):
    base = Decimal("1." + "0" * sign_count)
    result = num.quantize(base, rounding=ROUND_HALF_UP)
    return result.normalize()


def validate_expression(expression):
    errors = []

    if expression[0] in "*/":
        err = f"Started with unacceptable sign error: {expression[0]}."
        errors.append(err)

    if expression[-1] in OPERATORS:
        err = f"Ended with sign error: {expression[-1]}."
        errors.append(err)

    if not all(elem in ACCEPTABLE for elem in expression):
        err = "Contains unacceptable symbols"
        errors.append(err)

    space_between_digits = re.findall(r"\d\s+\d", expression)
    if space_between_digits:
        err = f"Spaces between digits errors: " \
              f"{'; '.join(space_between_digits)}."
        errors.append(err)

    signs_in_a_row = re.findall(r"[+\-*\/]+\s*[+\-*\/]+", expression)
    if signs_in_a_row:
        err = f"Signs in a row errors: {'; '.join(signs_in_a_row)}."
        errors.append(err)

    if not check_brackets_consistency(expression):
        err = "Brackets inconsistency"
        errors.append(err)

    return errors


def check_brackets_consistency(expression):
    stack = []
    for elem in expression:
        if elem == "(":
            stack.append(elem)
            continue
        elif stack:
            if stack[-1] == "(" and elem == ")":
                stack.pop()
                continue
            elif elem == ")":
                return False
        elif elem == ")":
            return False
    return not stack


def parse_expression(expression):
    """
    Gets arithmetical expression in str format, runs over the string,
    finds numbers, acceptable signs and brackets and sends it further in
    correct format
    """
    the_num = ""
    if expression[0] in OPERATORS:
        yield 0
    for elem in expression:
        if elem in NUMS:
            the_num += elem
        elif the_num:
            yield Decimal(the_num)
            the_num = ""
        if elem in OPERATORS or elem in BRACKETS:
            yield elem
    if the_num:
        yield Decimal(the_num)


def get_rpn(formula):
    """
    Function gets formula and returns the expression in Reverse Polish
    Notation
    """
    stack = []
    for symbol in formula:
        if symbol in OPERATORS:
            while stack and stack[-1] != "(" \
                    and OPERATORS[symbol][0] <= OPERATORS[stack[-1]][0]:
                yield stack.pop()
            stack.append(symbol)
        elif symbol == "(":
            stack.append(symbol)
        elif symbol == ")":
            while stack:
                elem = stack.pop()
                if elem == "(":
                    break
                yield elem
        else:
            yield symbol
    while stack:
        yield stack.pop()


def calculate_rpn(data):
    """
    Gets expression in Reverse Polish Notation and returns calculated
    result
    """
    stack = []
    for i, elem in enumerate(data):
        if elem in OPERATORS:
            num2, num1 = stack.pop(), stack.pop()
            stack.append(OPERATORS[elem][1](num1, num2))
        else:
            stack.append(elem)
    return stack[0]


def calculate_expression(expression):
    return math_round(calculate_rpn(get_rpn(parse_expression(expression))))
