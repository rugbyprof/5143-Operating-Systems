import random
import re
import argparse
import sys
import rich


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


class GenerateInstructions:
    def __init__(self):
        self.lowest_number = 1
        self.highest_number = 9
        self.length = 2

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
                code.append(f"LOAD R{reg_counter}, {token}")
                reg_counter += 1
            elif token in operators:
                reg1 = reg_counter - 2
                reg2 = reg_counter - 1
                code.append(f"{operators[token]} R{reg_counter}, R{reg1}, R{reg2}")
                reg_counter += 1

        # Assuming last operation result is in the last register used
        code.append(f"STORE R10, R{reg_counter-1}")
        return code

    def generate_instructions(
        self, size_kb, min_expression_length=3, max_expression_length=5
    ):
        """Generate a series of instructions with approximate total size."""
        generated_size = 0
        instructions = []

        while generated_size < size_kb * 1024:
            expr_length = random.randint(min_expression_length, max_expression_length)
            expr = self.random_expression(length=expr_length)
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

        registers = {}

        for i in range(12):
            registers[f"R{i}"] = int2bin(i)

        print(registers)

        binary_code = ""
        for line in assembly_code.split("\n"):
            parts = line.split()
            if parts[0] in opcodes:
                binary_code += opcodes[parts[0]]  # Add opcode
                for part in parts[1:]:
                    if part.startswith("R"):
                        binary_code += registers[part]  # Add register code
                    elif part.isdigit():
                        binary_code += format(
                            int(part), "08b"
                        )  # Convert immediate value to binary
            binary_code += "\n"

        return binary_code.strip()


# # Example usage
# assembly_code = """
# LOAD R1, 5
# ADD R3, R1, R2
# """
# binary_code = assembly_to_binary(assembly_code)
# print(binary_code)


if __name__ == "__main__":
    # kwargs, args = myKwargs(sys.argv)

    # size = kwargs.get("size", 2)

    # GI = GenerateInstructions()

    # instrs = GI.generate_instructions(size)
    # for instr in instrs:
    #     print(instr)

    registers = {}

    for i in range(12):
        registers[f"R{i}"] = int2bin(i)

    print(registers)
