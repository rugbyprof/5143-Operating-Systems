from rich import print
from collections.abc import MutableMapping
from random import randint
from alu import *


class Register:
    """Represents a single `register` with a read and write method
    to change the registers values.
    """

    def __init__(self):
        """Constructor"""
        self.contents = 0

    def write(self, x):
        """Change value of register"""
        self.contents = x

    def read(self):
        """Return value of register"""
        return self.contents

    def __add__(self, other):
        return self.contents + other.contents

    def __sub__(self, other):
        return self.contents - other.contents

    def __mul__(self, other):
        return self.contents * other.contents

    def __div__(self, other):
        return self.contents / other.contents

    def __str__(self):
        """Print out instance in readable format"""
        return f"[{self.contents}]"

    def __repr__(self):
        """Same as __str__"""
        return self.__str__()


class Registers(MutableMapping):
    """Represents a set of registers in an overloaded OOP fashion that
    allows for assignments to go like:

                r = Registers()
                r[0] = 44
                r[1] = 33


    Also each register has add,sub,mul,div overloaded so you can do:
    r[0] = r[0] + r[1]
    """

    __monostate = None

    def __init__(self, num=2):
        """Constructor"""

        if Registers.__monostate is not None:
            self.__dict__ = Registers.__monostate

        else:
            self.num = num
            self.registers = []
            for i in range(num):
                self.registers.append(Register())
            Registers.__monostate = self.__dict__

    def __setitem__(self, k, v):
        """Assigns a value to a particular register as long as the key is
        integer, and within bounds.
        """
        if isinstance(k, int) and k < self.num:
            # setattr(self, self.registers[k], v)
            self.registers[k].write(v)

    def __getitem__(self, k):
        """Returns a value from a specific register indexed by `k`"""
        if isinstance(k, int) and k < self.num:
            # getattr(self, k)
            return self.registers[k].read()
        return None

    def __len__(self):
        """Len() of object instance. Must be here to overload class
        instance or python chokes.
        """
        return self.num

    def __delitem__(self, k):
        """Overloads the del keyword to delete something out of a
        list or dictionary.
        """
        if isinstance(k, int):
            self.registers[k] = None

    def __iter__(self):
        """Allows object iteration, or looping over this object"""
        yield self.registers

    def __str__(self):
        s = "[ "
        i = 0
        for r in self.registers:
            s += f"R{i}{str(r)} "
            i += 1
        return s + "]"

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    reg1 = Registers(4)  # create 4 registers

    reg2 = Registers(4)  # create 4 registers

    reg3 = Registers(4)  # create 4 registers

    for i in range(len(reg2)):  # add random data to them
        reg2[i] = 10

    reg1[0] = reg1[0] + reg1[1]

    print(reg1)  # print them out
    print(reg2)  # print them out

    reg3[2] = 99

    print(reg1)
