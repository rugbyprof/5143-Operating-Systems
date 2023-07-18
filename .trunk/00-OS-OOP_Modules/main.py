from alu import ALU
from cpu import CPU
from memory import Memory
from pcb import PCB
from registers import Registers
from rich import print
import sys
from glob import glob


class Driver:
    def __init__(self, **kwargs):
        self.numRegisters = kwargs.get("numRegisters", 2)
        self.numProcesses = None
        self.processList = kwargs.get("processList", [])

        if len(self.processList) > 0:
            self.numProcesses = len(self.processList)
        else:
            print("Error: need a list of processes to load!")
            sys.exit()

        self.reg = Registers(self.numRegisters)
        self.mem = Memory()
        self.cpu = CPU()
        self.processes = []
        self.loadProcesses()

    def __str__(self):
        s = ""
        for k, v in self.__dict__.items():
            s += f"{k}:{v}\n"
        return s

    def __repr__(self):
        return self.__str__()

    def loadProcesses(self, processList=None):
        if not processList:
            processList = self.processList

        for process in processList:
            self.processes.append(PCB(exe=process))


if __name__ == "__main__":
    processList = sorted(glob("*.exe"))

    print(processList)

    d = Driver(processList=processList)

    print(d)
    # reg = Registers(2)
    # mem1 = Memory()
    # mem2 = Memory()
    # cpu = CPU()
    # pcb = PCB(exe="program_3.exe")

    # reg[0] = 9
    # reg[1] = 11

    # mem1[("C", 200)] = 999

    # print(reg)

    # while not pcb.eof():
    #     i = pcb.getCurrent()
    #     if "sleep" in i:
    #         pcb.inc()
    #         continue
    #     cpu.execute(i)
    #     pcb.inc()

    # print(mem1)
