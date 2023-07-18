"""
Usage:
    reg = Registers(2)
    alu = ALU()

    print(alu)

    reg[0] = 8
    reg[1] = 7

    print(reg)
    alu.execute("+")
    print(alu)
"""
import os
from rich import print


from registers import Registers


def add(l, r):
    """add left to right
    Params:
        l (int) : left arg
        r (int) : right arg
    Return:
        (int) answer
    """
    return l + r


def sub(l, r):
    """sub left from right
    Params:
        l (int) : left arg
        r (int) : right arg
    Return:
        (int) answer
    """
    return l - r


def mul(l, r):
    """mul left to right
    Params:
        l (int) : left arg
        r (int) : right arg
    Return:
        (int) answer
    """
    return l * r


def div(l, r):
    """div right into left
    Params:
        l (int) : left arg
        r (int) : right arg
    Return:
        (int) answer
    """
    return int(l / r)


class ALU(object):
    def __init__(self):
        """construct alu class
        Params:
            registers (Registers) : registers object
        """
        self.lhs = None
        self.rhs = None
        self.op = None
        self.registers = Registers()

        self.ops = {
            "ADD": add,
            "SUB": sub,
            "MUL": mul,
            "DIV": div,
            "+": add,
            "-": sub,
            "*": mul,
            "/": div,
        }

    def execute(self, op, targets=[]):
        """Execute instruction and store result in proper location.
        Params:
            op (string) : operation (add,sub,mul,div,+,-,*,/)
            targets (list) : index of registers to do op

            execute("+") will add reg0 and reg1
                or
            execute("-",[2,3]) will subtract reg3 from reg2

        """
        if len(targets) == 2:
            reg = targets

        self.lhs = self.registers[0]
        self.rhs = self.registers[1]
        self.op = op.upper()
        if self.op == "DIV" and self.rhs == 0:
            print(f"Division by zero! Op:{self.lhs}{op}{self.rhs}")
            return
        ans = self.ops[self.op](self.lhs, self.rhs)
        self.registers[0] = ans

    def __str__(self):
        """Print instance of ALU"""
        op = self.op
        if not op:
            op = "noop"

        return f"{self.registers[0]} {op} {self.registers[1]}"


if __name__ == "__main__":

    # create instance of 2 registers
    reg = Registers(2)

    # instantiate an ALU
    alu = ALU()

    # print alu but will have nothing
    # since registers are empty and no operation
    # has been set
    print(alu)

    # set values of register 1 and 2
    reg[0] = 8
    reg[1] = 7

    print(alu)

    alu.execute("+")
    print(alu)
