from rich import print


def add(l, r):
    return l + r


def sub(l, r):
    return l - r


def mul(l, r):
    return l * r


def div(l, r):
    return l / r


opLookup = {"ADD": add, "SUB": sub, "MUL": mul, "DIV": div}


class Register(object):
    def __init__(self, name=None):
        self.name = name
        self.contents = None
        self.val = None

    def __str__(self):
        return f"[{self.name}: {self.contents}]"

    def __repr__(self):
        return self.__str__()

    def load(self, value):
        self.set(value)

    def set(self, value):
        self.val = self.contents = value

    def __setattr__(self, __name: str, __value: int) -> None:
        self.__dict__[__name] = __value


class Alu(object):
    def __init__(self, registers):
        self.op = None
        self.lhs = None
        self.rhs = None
        self.registers = None

    def exec(self, instruction):

        self.lhs = self.registers

    def __str__(self):
        return f"{self.lhs} {self.op} {self.rhs}"


class Cpu:
    def __init__(self, numRegisters=2):
        self.cache = []
        self.pc = 0
        self.registers = {}
        for i in range(numRegisters):
            l = str(chr(i + 65))
            self.registers[l] = Register(l)

        self.alu = Alu()

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
    cpu = Cpu()

    print(cpu)
