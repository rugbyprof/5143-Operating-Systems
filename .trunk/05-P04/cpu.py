from rich import print
from registers import *
from randInstructions import RandInstructions
import sys


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


class Alu(object):
    def __init__(self, registers):
        """construct alu class
        Params:
            registers (Registers) : registers object
        """
        self.lhs = None
        self.rhs = None
        self.op = None
        if not isinstance(registers, Registers):
            print("Alu needs an instance of a registers class.")
            sys.exit()

        self.registers = registers
        self.ops = {"ADD": add, "SUB": sub, "MUL": mul, "DIV": div}

    def execute(self, op):
        """Execute instruction and store result in proper location.
        Params:
            op (string) : operation (add,sub,mul,div)
        """
        self.lhs = self.registers[0]
        self.rhs = self.registers[1]
        self.op = op.upper()
        ans = self.ops[self.op](self.lhs, self.rhs)
        self.registers[0] = ans

    def __str__(self):
        """Print instance of ALU"""
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


class ProgramCounter:
    def __init__(self):
        self.inst = 0
        self.line = 0


class Pcb:
    def __init__(self, **kwargs):
        kwargs.get()
        seed = 7763636
        inst = RandInstructions(seed)
        self.name = None
        self.inst = None
        self.pc = 0
        self.instructions = inst.getJson()
        self.registers = []

    def loadProgram(self, file_path):
        with open(file_path) as f:
            self.instructions = f.read()


if __name__ == "__main__":
    reg = Registers(2)
    cpu = Cpu(reg)

    print(cpu)

    reg[0] = 33
    reg[1] = 41

    alu = Alu(reg)

    alu.exec("add")
