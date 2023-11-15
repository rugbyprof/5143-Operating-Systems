import random
import re
import os
import sys


def myKwargs(argv):
    """This process command line arguments and lets you "configure" the current run.
    It takes parameters that look like: key=value or num_people=100 (with NO spaces between)
    and puts them into a python dictionary that looks like:
    {
        "key":"value",
        "num_people":100
    }

    If a parameter doesn't have an "=" sign in it, it puts it into a list
    Both the dictionary (kwargs) and list (args) get returned.
    See usage below under if__name__=='__main__'
    """
    kwargs = {}
    args = []
    for param in argv:
        if "=" in param:
            k, v = param.split("=")
            if v.isnumeric():
                kwargs[k] = int(v)
            else:
                kwargs[k] = v
        else:
            if param.isnumeric():
                param = int(param)
            args.append(param)

    return kwargs, args


def random_longest_math_expression(**kwargs):
    """
    lowest_number=1, highest_number=9, min_length=1, max_length=10
    Params:
        lowest_number (int)     : lowest decimal number for an expression
        highest_number (int)    : highest decimal number for an expression
        min_length (int)        :
        max_length (int)        :
    """

    lowest_number = kwargs.get("lowest_number", 1)
    highest_number = kwargs.get("highest_number", 9)
    min_length = kwargs.get("min_length", 1)
    max_length = kwargs.get("max_length", 10)

    # operators = ["^", "%", "*", "/", "+", "-"]
    operators = ["%", "*", "/", "+", "-"]
    operands = [
        random.randint(lowest_number, highest_number)
        for _ in range(random.randint(min_length, max_length))
    ]
    expression = ""
    for i in range(len(operands) - 1):
        flag = random.choice([True, False])
        operator = random.choice(operators)
        operator2 = random.choice(operators)
        if flag:
            expression += f" ({operands[i]} {operator} "
        else:
            expression += f"{operands[i]} {operator} "
        operator = random.choice(operators)
        expression += str(operands[-1])
        flag = random.choice([True, False])
        parenthesis_count = expression.count("(")
        parenthesis_count -= expression.count(")")
        for _ in range(parenthesis_count):
            expression += ")"
            expression += " " + str(operator) + " "
    expression += str(operands[-1])
    parenthesis_count = expression.count("(")
    parenthesis_count -= expression.count(")")
    for _ in range(parenthesis_count):
        expression += ")"
    return expression


def string_to_decimal_list(text):
    return [ord(char) - 30 for char in text]


def decimal_list_to_string(decimal_list):
    return "".join(chr(decimal + 30) for decimal in decimal_list)


if __name__ == "__main__":
    kwargs, args = myKwargs(sys.argv)

    print(kwargs)

    ln = kwargs.get("ln", 1)
    hn = kwargs.get("hn", 9)
    minl = kwargs.get("minl", 1)
    maxl = kwargs.get("maxl", 10)

    longest_expression = random_longest_math_expression(
        lowest_number=ln, highest_number=hn, min_length=minl, max_length=maxl
    )
    # operator = random.choice(["^", "%", "*", "/", "+", "-"])
    operator = random.choice(["%", "*", "/", "+", "-"])
    result = re.sub(r"(\d+) \s*\(", r"\1 " + operator + " (", longest_expression)
    longest_expression = re.sub(r"\) \s*\(", ") " + operator + " (", result)
    # print(longest_expression)
    while "^" in longest_expression:
        longest_expression = longest_expression.replace("^", "**")
    # print(longest_expression)
    try:
        answer = eval(longest_expression)
    except Exception as ex:
        answer = "Error:" + str(ex)

    os.system("clear")
    text = longest_expression
    result = string_to_decimal_list(text)
    print("\nDecimal List - " + str(result))
    text = decimal_list_to_string(result)
    print("\nEquation: " + text)
    print("\nAnswer: " + str(answer))
    print("\n\n\n\n\n")
