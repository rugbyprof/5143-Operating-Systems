import os

from alu import ALU
from clock import Clock
from memory import Memory
from pcb import PCB
from randInstructions import RandInstructions
from registers import Registers


from rich import print
import sys


class CPU(object):
    def __init__(self):
        self.alu = ALU()
        self.busy = False
        self.cache = []
        self.clock = Clock()
        self.memory = Memory()
        self.pcb = None
        self.registers = Registers()

    def contextSwitch(self, pcb=None):
        self.busy = False
        self.pcb = None
        if pcb:
            if not isinstance(pcb, PCB):
                sys.exit("Error: pcb is not an instance of PCB")
            self.busy = True
            self.pcb = pcb

    # def load(self):
    #     self.inst = self.pcb.getInst()
    #     self.instSize = len(self.inst)

    """needs fixin!!
    """

    def execute(self, inst):
        i, loc, reg = inst.split()

        # print(f"{inst} {loc} {reg} ")
        # breaking up inst
        memBlock = loc[0]
        memAddr = loc[1:]
        register = int(reg[1]) - 1

        # loads registers
        if i == "READ":
            print(
                f"reading from: [{memBlock}][{memAddr}] => {self.memory[(str(memBlock), int(memAddr))]}"
            )
            self.registers[register] = self.memory[(str(memBlock), int(memAddr))]

        if i in ["ADD", "SUB", "MUL", "DIV"]:
            print(f"executing: {i}")
            self.alu.execute(i)
            print(self.registers)

        if i == "WRITE":
            print(
                f"self.memory[({str(memBlock)}, {int(memAddr)})] = {self.registers[0]}"
            )
            self.memory[(str(memBlock), int(memAddr))] = self.registers[0]

    def __str__(self):
        return f"[{self.registers}{self.alu}]"


if __name__ == "__main__":
    reg = Registers(2)
    mem1 = Memory()
    mem2 = Memory()
    cpu = CPU()
    pcb = PCB(exe="program_3.exe")

    reg[0] = 9
    reg[1] = 11

    mem1[("C", 200)] = 999

    print(reg)

    while not pcb.eof():
        i = pcb.getCurrent()
        if "sleep" in i:
            pcb.inc()
            continue
        cpu.execute(i)
        pcb.inc()

    print(mem1)
