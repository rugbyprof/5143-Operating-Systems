from rich import print
from registers import *


def add(l, r):
    return l + r


def sub(l, r):
    return l - r


def mul(l, r):
    return l * r


def div(l, r):
    return l / r


class Alu(object):
    def __init__(self, registers):
        self.lhs = None
        self.rhs = None
        self.op = None
        self.registers = registers
        self.ops = {"ADD": add, "SUB": sub, "MUL": mul, "DIV": div}

    def exec(self, op):
        self.lhs = self.registers[0]
        self.rhs = self.registers[1]
        self.op = op.upper()
        ans = self.ops[self.op](self.lhs, self.rhs)
        self.registers[0] = ans

    def __str__(self):
        return f"{self.lhs} {self.op} {self.rhs}"


class Cpu:
    def __init__(self, registers):
        self.cache = []
        self.pc = 0
        self.registers = registers
        self.alu = Alu(registers)

    def loadProcess(self, pcb):
        pass

    def __str__(self):
        return f"[{self.registers}{self.alu}]"


class Pcb(object):
    def __init__(self):
        self.name = None
        self.inst = None
        self.pc = 0


if __name__ == "__main__":
    reg = Registers(2)
    cpu = Cpu(reg)

    print(cpu)

    reg[0] = 33
    reg[1] = 41

    alu = Alu(reg)

    alu.exec("add")
