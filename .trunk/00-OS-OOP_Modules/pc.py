"""PC - Program Counter
Usage:


"""
import json
import sys
from rich import print


class PC(object):
    def __init__(self):
        self.current = 0
        self.subCurrent = 0
        self.instData = {}
        self.eof = False
        self.totalLines = 0
        self.instCount = 0

    def init(self, instructions):
        i = 0
        for inst in instructions:
            self.totalLines += len(inst)
            self.instData[i] = {"inst": inst, "lines": len(inst)}
            i += 1
        self.instCount = i - 1
        self.current = 0
        self.subCurrent = 0

    def inc(self):
        """
        Usage:
            inc(0.09)
        """
        self.subCurrent += 1
        if self.subCurrent == self.getInstSize():
            self.current += 1
            self.subCurrent = 0

        if self.current < len(self.instData):
            if self.subCurrent < self.getInstSize():
                self.eof = False
                return True

        self.eof = True
        return False

    def getInstSize(self, current=None):
        if not current:
            current = self.current

        if not self.eof:
            return len(self.instData[self.current]["inst"])

        return None

    def getNext(self):
        self.inc()
        return self.getCurrent()

    def getCurrent(self):
        if not self.eof:
            return self.instData[self.current]["inst"][self.subCurrent]

    def getPc(self):
        return {"inst": self.current, "line": self.subCurrent}

    def setInst(self, i):
        self.current = i
        self.subCurrent = 0

    def setLine(self, l):
        """Set the subCounter that points to a specific"""
        self.subCurrent = l

    def __str__(self):
        inst = None
        if not self.eof:
            inst = {self.instData[self.current]["inst"][self.subCurrent]}
        return f"[pc: {str(self.current)}.{str(self.subCurrent)} , instCount: {self.instCount} , totalLines: {self.totalLines} , inst: {inst} , eof: {self.eof}]"

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":

    pc = PC()

    with open("program_0.exe") as f:
        instructions = json.load(f)
        pc.init(instructions)

    while not pc.eof:
        # print(pc.getPc())
        inst = pc.getCurrent()
        print(pc)
        pc.inc()

        print(str(pc))
