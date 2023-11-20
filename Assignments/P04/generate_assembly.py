import random
import re
import os
import sys

import random
from rich import print


#################UNUSED#####################
def string_to_decimal_list(text):
    return [ord(char) - 30 for char in text]


def decimal_list_to_string(decimal_list):
    return "".join(chr(decimal + 30) for decimal in decimal_list)


def parse_expression(expression):
    # This function will parse the expression '3 + 4 - 7' into ['3', '+', '4', '-', '7']
    return [part.strip() for part in expression.split()]


#################UNUSED#####################

def evaluate_postfix(expression):
    opDict = {
        "+": lambda x,y: x+y,
        "-": lambda x,y: x-y,
        "*": lambda x,y: x*y,
        "/": lambda x,y: x/y,
        "%": lambda x,y: x%y,
        "^": lambda x,y: x**y
    }

    # Create an empty stack to store operands
    stack = []

    # Iterate through each token in the expression
    for token in expression.split():
        if token.isdigit():
            # If the token is an operand, push it onto the stack
            stack.append(int(token))
        else:
            # If the token is an operator, pop the top two operands from the stack
            operand2 = stack.pop()
            operand1 = stack.pop()
            
            if not token in opDict:
                raise ValueError(f"Unsupported operator: {token}")
            
            if token == '/' and operand2 == 0:
                raise ValueError("Division by zero is not allowed")
            
            result = opDict[token](operand1,operand2)                    

            # Push the result back onto the stack
            stack.append(result)

    # The final result should be the only item left in the stack
    if len(stack) != 1:
        raise ValueError("Invalid expression")

    return stack[0]



class RPNToAssembly:
    def __init__(self):
        self.register_count = 0
        self.instructions = []

    def _get_next_register(self):
        self.register_count += 1
        return f"R{self.register_count}"

    def _load_operand(self, operand):
        reg = self._get_next_register()
        self.instructions.append(f"LOAD {reg} {operand}")
        return reg

    def _perform_operation(self, operator, reg1, reg2):
        if operator == "+":
            self.instructions.append(f"ADD {reg1} {reg1} {reg2}")
        elif operator == "-":
            self.instructions.append(f"SUB {reg1} {reg1} {reg2}")
        elif operator == "*":
            self.instructions.append(f"MUL {reg1} {reg1} {reg2}")
        elif operator == "/":
            self.instructions.append(f"DIV {reg1} {reg1} {reg2}")
        elif operator == "%":
            self.instructions.append(f"MOD {reg1} {reg1} {reg2}")
        # elif operator == "^":
        #     self.instructions.append(f"POW {reg1} {reg1} {reg2}")
        # Add more operations (like '-', '/') as needed
        return reg1

    def generate_assembly(self, rpn_expression):
        print(f"RPN: {rpn_expression}")
        tokens = rpn_expression.split()
        stack = []

        for token in tokens:
            print(f"Token: {token}")
            if token.isnumeric():  # Operand
                reg = self._load_operand(token)
                stack.append(reg)
            else:  # Operator
                reg2 = stack.pop()
                reg1 = stack.pop()
                result_reg = self._perform_operation(token, reg1, reg2)
                stack.append(result_reg)

        return self.instructions


class ShuntingYard:
    def __init__(self):
        self.precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "%":2 ,"^": 3}
        self.associativity = {"+": "L", "-": "L", "*": "L", "/": "L", "%": "L","^": "R"}

    def convert_to_rpn(self, expression):
        output = []
        operator_stack = []

        tokens = expression.split()

        for token in tokens:
            if token.isnumeric():
                output.append(token)
            elif token in self.precedence:
                while (
                    operator_stack
                    and operator_stack[-1] != "("
                    and (
                        (
                            self.associativity[token] == "L"
                            and self.precedence[token]
                            <= self.precedence[operator_stack[-1]]
                        )
                        or (
                            self.associativity[token] == "R"
                            and self.precedence[token]
                            < self.precedence[operator_stack[-1]]
                        )
                    )
                ):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == "(":
                operator_stack.append(token)
            elif token == ")":
                while operator_stack and operator_stack[-1] != "(":
                    output.append(operator_stack.pop())
                operator_stack.pop()  # Pop the '('

        while operator_stack:
            output.append(operator_stack.pop())

        return " ".join(output)


def add_random_parentheses(expression):
    tokens = expression.split()
    num_tokens = len(tokens)

    # Potential positions for parentheses (around binary expressions)
    binary_expr_positions = [(i, i + 2) for i in range(0, num_tokens - 2, 2)]

    # Randomly select positions to add parentheses
    selected_positions = random.sample(
        binary_expr_positions, k=random.randint(1, len(binary_expr_positions) // 2)
    )

    # Add parentheses
    for start, end in selected_positions:
        tokens[start] = "( " + tokens[start]
        tokens[end] = tokens[end] + " )"

    return " ".join(tokens)


class RegisterSet:
    """Barebones class to assign and use/re-use available registers"""

    def __init__(self, size=10):
        self.registers = [False] * size  # False indicates the register is available

    def get_next_available(self):
        for i, used in enumerate(self.registers):
            if not used:
                self.registers[i] = True  # Mark register as used
                return f"R{i+1}"
        raise Exception("No available registers")

    def release_register(self, register):
        index = int(register[1:]) - 1
        if 0 <= index < len(self.registers):
            self.registers[index] = False
        else:
            raise Exception("Invalid register")


def binary_to_hex(binary_str):
    """
    Convert a binary string of varying length (multiple of 4) to hexadecimal.

    Parameters:
    binary_str (str): A binary string with length as a multiple of 4.

    Returns:
    str: The hexadecimal representation of the binary string.
    """
    # Check if the length of the binary string is a multiple of 4
    if len(binary_str) % 4 != 0:
        print(f"Binary: {binary_str}")
        print(len(binary_str))
        print(len(binary_str) % 4)
        raise ValueError("The length of the binary string must be a multiple of 4.")

    # Initializing the hexadecimal string
    hex_str = ""
    # Process each 4-bit chunk
    for i in range(0, len(binary_str), 4):
        chunk = binary_str[i : i + 4]

        # convert string binary to integer base 2
        hex_digit = int(chunk, 2)
        # then convert back to string AND append while stripping off the 0x with [2:]
        hex_str += str(hex(hex_digit))[2:].upper()

    return hex_str




def isInt(s):
    """
    Test if a string can be converted to an integer.

    Parameters:
    s (str): The string to test.

    Returns:
    bool: True if the string can be converted to an integer, False otherwise.
    """

    # Stripping whitespaces and checking for negative numbers
    s = s.strip()
    if s.startswith("-") and s[1:].isdigit():
        return True

    # Using try-except block to check for conversion
    try:
        int(s)
        return True
    except ValueError:
        return False


def register2Bin(regID):
    """Converts a register id (R1-R10) to a 4 digit binary string
    R1  = 0001
    R2  = 0010
    ...
    R10 = 1010
    """
    return format(int(regID[1:]), "04b")


def random_math_expression(**kwargs):
    """
    lowest_number=1, highest_number=9, min_length=1, max_length=10
    Params:
        lowest_number (int)     : lowest decimal number for an expression
        highest_number (int)    : highest decimal number for an expression
        min_length (int)        : min number of operators
        max_length (int)        : max number of operators

    """
    lowest_number = kwargs.get("lowest_number", 1)
    highest_number = kwargs.get("highest_number", 9)
    min_length = kwargs.get("min_length", 2)
    max_length = kwargs.get("max_length", 4)
    
    if max_length < min_length:
        max_length = min_length
        
    operators = ["%", "*", "/", "+", "-"] #,"^"
    
    print(min_length, max_length)
    length = random.randint(min_length, max_length)

    # Ensuring the length of the expression
    operands = [
        random.randint(lowest_number, highest_number) for _ in range(length + 1)
    ]
    expression_parts = []

    for i in range(length):
        print(i)
        expression_parts.append(str(operands[i]))
        expression_parts.append(random.choice(operators))

    expression_parts.append(str(operands[-1]))

    # Adding parentheses to ensure binary expressions
    # for _ in range(length - 1):
    #     insert_position = random.choice(
    #         [i for i in range(1, len(expression_parts) - 1, 2)]
    #     )
    #     expression_parts.insert(insert_position - 1, "(")
    #     expression_parts.insert(insert_position + 3, ")")

    return " ".join(expression_parts)


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


def expression_to_assembly(expression, register_set):
    """Turns a simple arithmetic expression into our pseudo assembly.
    Params:
        expression (string) : basic arithmetic expressions without parans
        register_set (RegisterSet) : Registers class to help determine open or busy registers
    Example:
        Exp: 4 / 9 - 3 + 4
        Ass:    LOAD R1 4       # load 4 into register 1
                LOAD R2 9       # load 9 into register 2
                DIV R3 R1 R2    # divide 4/9 and store answer in register 3
                LOAD R1 3       # load register 1 with 3
                SUB R4 R3 R1    # subtract register 1 from register 3 put answer in register 4
                LOAD R3 4       # load register three with 4
                ADD R5 R4 R3    # add register 4 and register 3 and store answer in register 5
        Answer: Will be in R5
    Returns:
        (list) : containing similar assembly instructions that you see above.
    """
    operators = {"%": "MOD", "*": "MUL", "/": "DIV", "+": "ADD", "-": "SUB"} #"^":"EXP"

    parts = expression.split()
    assembly_instructions = []

    # Load the first operand
    reg1 = register_set.get_next_available()
    assembly_instructions.append(f"LOAD {reg1} {parts[0]}")

    for i in range(1, len(parts), 2):
        operator = operators[parts[i]]
        operand = parts[i + 1]

        # Load the next operand
        reg2 = register_set.get_next_available()
        assembly_instructions.append(f"LOAD {reg2} {operand}")

        # Perform the operation
        result_reg = register_set.get_next_available()
        assembly_instructions.append(f"{operator} {result_reg} {reg1} {reg2}")

        # Release the previous registers if not needed
        register_set.release_register(reg1)
        reg1 = result_reg  # Store the result for the next operation

    return assembly_instructions


def assembly_to_binary(assembly_code):
    """Converts all parts of a pseudo assembly instruction to a binary string using 4 bit opcodes.
    Params:
        assembly_code (list) : list of pseudo assembly instructions
    Returns:
        Hex (str) : hex version of the assembly
    Example:
        Exp: ['LOAD R1 4', 'LOAD R2 9', 'DIV R3 R1 R2', 'LOAD R1 3', 'SUB R4 R3 R1', 'LOAD R3 4', 'ADD R5 R4 R3']
        Hex: A14A29E312A13C431A34B543
    """
    opcodes = {
        "LOAD": "1010",
        "ADD": "1011",
        "SUB": "1100",
        "MUL": "1101",
        "DIV": "1110",
        "MOD": "1111",
    }

    binary_code = []

    for line in assembly_code:
        binStr = []
        parts = line.split()

        # opcode is like add, sub, mul ....
        opcode = opcodes[parts[0]]

        # add first four binary digits to our binary string
        binStr.append(opcode)
        for val in parts[1:]:
            if "R" in val:
                # Converts R1-R10 to some 4 digit binary equivalent of just the integer
                binStr.append(register2Bin(val))
            elif isInt(val):
                # formats an integer to a 4 digit binary string with leading zeros
                val = format(int(val), "04b")

                binStr.append(val)
        binary_code.append("".join(binStr))
    return binary_code


def GenerateAssembly(**kwargs):
    """Generates a random math expression and converts it to assembly and binary.
    Params:
        None
    Returns:
        (str) : hex version of the assembly
    """
    expression = kwargs.get("expression", None)
    min_length = kwargs.get("min_length", 3)
    max_length = kwargs.get("max_length", 5)
    lowest_number = kwargs.get("lowest_number", 1)
    highest_number = kwargs.get("highest_number", 9)
    
    expression = random_math_expression(min_length=min_length, max_length=max_length,highest_number=highest_number,lowest_number=lowest_number) 
    shunting_yard = ShuntingYard()
    postfix_exp = shunting_yard.convert_to_rpn(expression)
    rpn_to_assembly = RPNToAssembly()
    assembly_code = rpn_to_assembly.generate_assembly(postfix_exp)
    binary = assembly_to_binary(assembly_code)
    hexstr = ""
    for bin in binary:
        hexstr += binary_to_hex(bin)
    return hexstr

if __name__ == "__main__":
    kwargs, args = myKwargs(sys.argv)
    
    
    expression = kwargs.get("expression", None)
    min_length = kwargs.get("min_length", 3)
    max_length = kwargs.get("max_length", 5)
    lowest_number = kwargs.get("lowest_number", 1)
    highest_number = kwargs.get("highest_number", 9)
    
    print("=" * 40)

    shunting_yard = ShuntingYard()
    register_set = RegisterSet(size=10)
    if not expression:
        expression = random_math_expression(min_length=min_length, max_length=max_length)
        #print(f"Rand: {expression}")
        expression = add_random_parentheses(expression)
    print(f"Parens: {expression}")
    postfix_exp = shunting_yard.convert_to_rpn(expression)
    print(f"Rpn: {postfix_exp}")
    
    result = evaluate_postfix(postfix_exp)
    print(f"Result of '{postfix_exp}' is {result}")

    # Test the class
    rpn_to_assembly = RPNToAssembly()
    rpn_expression = postfix_exp
    assembly_code = rpn_to_assembly.generate_assembly(rpn_expression)
    for instruction in assembly_code:
        print(instruction)

    # assembly_code = expression_to_assembly(expression, register_set)
    print(f"Ass: {assembly_code}")
    binary = assembly_to_binary(assembly_code)
    print(f"Bin: {binary}")
    hexstr = ""
    for bin in binary:
        print(f"Bin: {bin} Hex: {binary_to_hex(bin)}")
        hexstr += binary_to_hex(bin)
    print(f"All Hex: {hexstr}")
    print("=" * 40)
