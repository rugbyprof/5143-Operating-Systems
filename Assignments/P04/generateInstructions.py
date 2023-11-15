import random
import re
import argparse
import sys
from rich import print


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


def int2bin(intNum, padding=4):
    return bin(intNum)[2:].zfill(padding)


class Register:
    _global_id = 0
    _registers = []

    def __init__(self):
        self.id = Register._global_id
        Register._global_id += 1
        Register._registers.append(self)

        self.in_use = False  # Indicates whether the register is currently in use
        self.value = None  # The value held by the register

    def set_value(self, value):
        self.value = value
        self.in_use = True

    def release(self):
        self.value = None
        self.in_use = False

    def __repr__(self):
        return f"Register(ID: {self.id}, In Use: {self.in_use}, Value: {self.value})"

    @classmethod
    def get_all_registers(cls):
        return cls._registers

    # # Example Usage
    # reg1 = Register()
    # reg1.set_value(100)

    # reg2 = Register()
    # reg2.set_value(200)

    # print(reg1)  # Output: Register(ID: 0, In Use: True, Value: 100)
    # print(reg2)  # Output: Register(ID: 1, In Use: True, Value: 200)

    # reg1.release()
    # print(reg1)  # Output: Register(ID: 0, In Use: False, Value: None)

    # # Optional: Get all registers
    # all_registers = Register.get_all_registers()
    # print(all_registers)

    def __str__(self):
        return f"Occupied: {self.occupied}, Value: {self.value}"


class Registers:
    def __init__(self, num_registers=10):
        self.num_registers = num_registers
        self.registers = [Register() for x in range(self.num_registers)]

    def __str__(self):
        s = ""
        for r in self.registers:
            s += str(r)
        return s


class GenerateInstructions:
    """Method written by Srinivas!!"""

    def __init__(self):
        self.lowest_number = 1
        self.highest_number = 9
        self.length = 2
        self.registers = {}
        self.expressions = []

        for i in range(10):
            self.registers[str(f"R{i}")] = int2bin(i)

    def random_expression(self, lowest_number=None, highest_number=None, length=None):
        """Generate a random arithmetic expression.
        Params:
            lowest_number (int): the lowest int to use like a 1 or 2 or a 9....
            hight_numner (int): the highest number to use like a 8,9 or even bigger!
                I try and stick with integers between 1-9
            length (int) : how many operations. 3 could be for example:  1 + 2 + 3
        """
        if not lowest_number:
            lowest_number = self.lowest_number

        if not highest_number:
            highest_number = self.highest_number

        if not length:
            length = self.length

        operators = ["%", "*", "/", "+", "-"]
        expression = ""
        for _ in range(length):
            num = random.randint(lowest_number, highest_number)
            op = random.choice(operators)
            expression += f"{num} {op} "
        expression += str(random.randint(lowest_number, highest_number))
        return expression.strip()

    def convert_to_assembly(self, expression):
        """Convert arithmetic expression to pseudo-assembly code.
        Params:
            expression (str) : arithmetic expression to be converted to pseudo assembly
        Returns:
            str :
        """
        operators = {"+": "ADD", "-": "SUB", "*": "MUL", "/": "DIV", "%": "MOD"}
        tokens = expression.split()
        code = []
        reg_counter = 1

        for token in tokens:
            if token.isdigit():
                code.append(f"LOAD R{reg_counter} {token}")
                reg_counter += 1
            elif token in operators:
                reg1 = reg_counter - 2
                reg2 = reg_counter - 1
                code.append(f"{operators[token]} R{reg_counter} R{reg1} R{reg2}")
                reg_counter += 1

        # Assuming last operation result is in the last register used
        code.append(f"STORE R10 R{reg_counter-1}")
        return code

    def generate_instructions(
        self, size_kb, min_expression_length=3, max_expression_length=5
    ):
        """Generate a series of instructions with approximate total size.
        Params:
            size_kb (int)                   : some approximation of a size in kb
            min_expression_length (int)     : min number of operands in expression,
            max_expression_length (int)     : max number of operands in expression,
        Returns:
            list of pseudo assembly instructions

        """
        generated_size = 0
        instructions = []

        while generated_size < size_kb * 1024:
            expr_length = random.randint(min_expression_length, max_expression_length)
            expr = self.random_expression(length=expr_length)
            self.expressions.append(expr)
            asm = self.convert_to_assembly(expr)
            instructions.extend(asm)
            generated_size += sum(
                len(line) for line in asm
            )  # Approximate size in bytes

        return instructions

    def assembly_to_binary(self, assembly_code):
        """
        operators = {"+": "ADD", "-": "SUB", "*": "MUL", "/": "DIV", "%": "MOD"}
        """
        opcodes = {
            "LOAD": "0001",
            "ADD": "0010",
            "SUB": "0011",
            "MUL": "0100",
            "DIV": "0101",
            "MOD": "0110",
        }

        binary_code = []

        if isinstance(assembly_code, str):
            assembly_code = assembly_code.split("\n")
        i = 0
        for line in assembly_code:
            binary = ""
            tmp = ""
            parts = line.split(" ")
            if parts[0] in opcodes:
                binary += opcodes[parts[0]]  # Add opcode
                for part in parts[1:]:
                    tmp += part
                    if part.startswith("R"):
                        binary += self.registers[part]  # Add register code
                    elif part.isdigit():
                        binary += format(
                            int(part), "08b"
                        )  # Convert immediate value to binary
            print(f"{i}: {line}")
            i += 1
            if binary:
                binary_code.append(binary)

        return binary_code


if __name__ == "__main__":
    kwargs, args = myKwargs(sys.argv)

    size = kwargs.get("size", 4)
    minlen = kwargs.get("minlen", 3)
    maxlen = kwargs.get("maxlen", 6)

    GI = GenerateInstructions()

    instrs = GI.generate_instructions(size, minlen, maxlen)
    for i in range(len(GI.expressions)):
        print(f"{i}: {GI.expressions[i]}")

    print(instrs)

    binary_code = GI.assembly_to_binary(instrs)
    print(binary_code)
