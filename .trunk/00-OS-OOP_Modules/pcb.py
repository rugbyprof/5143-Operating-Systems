from registers import *
from misc import id
from randInstructions import *
import os
import json
from rich import print

from pc import PC


class PCB:
    def __init__(self, **kwargs):
        self.exe = kwargs.get("exe", None)
        self.id = kwargs.get("id", id())
        self.name = kwargs.get("name", None)
        self.seed = kwargs.get("seed", 7763636)

        self.pc = PC()

        # if no exe to load, generate a random one
        if not self.exe:
            self.instructions = kwargs.get(
                "instructions", RandInstructions(seed=self.seed)
            )
            if isinstance(self.instructions, RandInstructions):
                self.instructions = self.instructions.getJson()
        # load the exe
        else:
            if os.path.isfile(self.exe):
                self.loadProgram(self.exe)
            else:
                print("Error: exe: {self.exe} is not a valid file!")

    def loadProgram(self, file_path):
        """loadProgram: loads a file of instructions"""
        with open(file_path) as f:
            self.instructions = json.load(f)
            self.pc.init(self.instructions)

    def getCurrent(self):
        return self.pc.getCurrent()

    def inc(self):
        """Increments the program counter
        Params:
            None
        """
        return self.pc.inc()

    def eof(self):
        return self.pc.eof

    def __str__(self):
        s = ""
        s += f"seed: {self.seed}\n"
        s += f"name: {self.name}\n"
        s += f"id: {self.id}\n"
        s += f"pc: {str(self.pc)}\n"
        return s

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    pcb = PCB(exe="program_0.exe")

    print(pcb)

    while not pcb.pc.eof:
        print(pcb.pc.getCurrent())
        pcb.inc()

    print(pcb)
