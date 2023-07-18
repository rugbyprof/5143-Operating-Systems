from rich import print
from collections.abc import MutableMapping
from random import randint
import os

from borg import Borg

"""
A single borg instance of our convoluted memory. It is configurable but defaults
stick to the values we used in our simulations.
"""


class Memory(MutableMapping):
    __monostate = None

    def __init__(self, **kwargs):
        """Constructor"""

        if Memory.__monostate is not None:
            self.__dict__ = Memory.__monostate
        else:
            self.sections = kwargs.get("sections", ["A", "B", "C"])
            self.memRange = kwargs.get("memRange", [100, 255, 5])
            self.minMemAddr = self.memRange[0]
            self.maxMemAddr = self.memRange[1]
            self.loadRandVals = kwargs.get("loadRandVals", True)

            self.memory = {}
            start, stop, step = self.memRange
            for section in self.sections:
                self.addSection(section, start, stop, step)
            Memory.__monostate = self.__dict__

    def addSection(self, section, start=None, stop=None, step=None):
        if not start:
            start = int(self.memRange[0])
        if not stop:
            stop = int(self.memRange[1])
        if not step:
            step = int(self.memRange[2])

        self.memory[section] = {}
        for i in range(start, stop, step):
            if self.loadRandVals:
                r = randint(1, 9)
            self.memory[section][i] = r

    def getRange(self, sec, start=None, stop=None):
        if not start:
            start = self.memRange[0]
        if not stop:
            stop = self.memRange[1]

        result = {}
        for k, v in self.memory[sec].items():
            if k >= start and k <= stop:
                result[k] = v

        return result

    def __setitem__(self, k, v):
        """Assigns a value to a particular memory location"""
        if isinstance(k, tuple):
            # setattr(self, self.registers[k], v)
            key = k[0]
            addr = k[1]
            if key in self.memory:
                if addr in self.memory[key]:
                    self.memory[key][addr] = v

    def __getitem__(self, k):
        """Returns a value from a specific memory location`"""
        if isinstance(k, tuple):
            # setattr(self, self.registers[k], v)
            key = k[0]
            addr = k[1]
            if key in self.memory:
                if addr in self.memory[key]:
                    return self.memory[key][addr]
            return None

    def __len__(self):
        """Len() of object instance. Must be here to overload class
        instance or python chokes.
        """
        return len(self.memory)

    def __delitem__(self, k):
        """Overloads the del keyword to delete something out of a
        list or dictionary.
        """
        if isinstance(k, tuple):
            # setattr(self, self.registers[k], v)
            key = k[0]
            addr = k[1]
            if key in self.memory:
                if addr in self.memory[key]:
                    self.memory[key][addr] = None

    def __iter__(self):
        """Allows object iteration, or looping over this object"""
        yield self.memory

    def __str__(self):
        s = ""
        for sec in self.memory:
            for address, value in self.memory[sec].items():
                s += f"{sec}[{address}] = {value}\n"
            s += "\n"
        return s

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    m = Memory()

    print(m)

    m.addSection("P")

    print(m)

    print(m.getRange("A", 125, 200))

    m[("P", 200)] = 99

    print(m)

    print(m[("P", 200)])
