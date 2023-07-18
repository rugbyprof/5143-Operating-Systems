from random import shuffle, randint
import json
import random
from datetime import datetime


def buildRandomChoiceList(ratio):

    chances = []
    ptrue = int(ratio * 100)
    pfalse = 100 - ptrue
    for _ in range(ptrue):
        chances.append(1)
    for _ in range(pfalse):
        chances.append(0)
    return chances


class RandInstructions:
    def __init__(self, **kwargs):
        """
        I want to generate instructions that are basically a single double or
        triple instruction.
        Where:
            1 = (2 reads, 1 op, 1 write)
            2 = (4 reads, 2 ops, 2 writes)
            3 = (6 reads, 3 ops, 3 writes)

        So I generate a list like [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3]
        which weighs more towards a single length instruction. When shuffled
        it looks like: [2, 3, 1, 1, 1, 3, 1, 2, 1, 1, 1, 2]. Now every time
        I generate an instruction, shuffle the list and choose the first value
        to determine instruction size.
        """

        # Build my list to determine instruction length
        shortInst = [1] * 7
        medInst = [2] * 3
        longInst = [3] * 2
        self.instLength = shortInst + medInst + longInst

        # get a seed from kwargs or use system time
        # this allows us to generate same output if necessary
        self.seed = kwargs.get("seed", datetime.now().timestamp())
        random.seed(self.seed)

        # pull possible params from kwargs to tailor the building of
        # instructions
        self.addressRange = kwargs.get("addressRange", (100, 255, 5))
        self.choices = kwargs.get("choices", ["ADD", "SUB", "MUL", "DIV"])
        self.genAmount = kwargs.get("genAmount", 1000)
        self.memblocks = kwargs.get("memblocks", ["A", "B", "C"])
        self.registers = kwargs.get("registers", ["R1", "R2"])
        self.outFilePattern = kwargs.get("outFile", "program_")
        self.keepInstLocal = kwargs.get("keepInstLocal", False)
        self.privilegedRatio = kwargs.get("privilegedRatio", 0)
        self.numProcesses = kwargs.get("numProcesses", 1)
        self.sleepRatio = kwargs.get("sleepRatio", 0)
        self.sleepRange = kwargs.get("sleepRange", [5, 15])

        # print(self.privilegedRatio)
        self.privelegedChances = [0]
        if self.privilegedRatio > 0:
            self.privelegedChances = buildRandomChoiceList(self.privilegedRatio)

        # print(self.sleepRatio)
        self.sleepChances = [0]
        if self.sleepRatio > 0:
            self.sleepChances = buildRandomChoiceList(self.sleepRatio)

        self.processInstructions = {}

        for i in range(self.numProcesses):
            self.processInstructions[i] = []

        # print(self.privelegedChances)

        # build list to randomly choose memory addresses within proper range
        start, stop, step = self.addressRange
        self.memaddress = [x for x in range(start, stop, step)]

        # init vars that hold generated instructions
        self.strInstructions = ""
        self.listInstructions = []

        # shuffle all appropriate lists
        self.shuffleChoices()
        # generate the intructions
        self.generateInstructions()

    def shuffleChoices(self):
        """Shuffles all lists that need shuffling."""
        shuffle(self.instLength)
        shuffle(self.choices)
        shuffle(self.registers)
        shuffle(self.memblocks)
        shuffle(self.memaddress)
        shuffle(self.privelegedChances)
        shuffle(self.sleepChances)

    def generateInstructions(self, num=None):
        """
        Params:
            num (int) : number of instructions to generate
        """
        pCount = 0
        # no num passed in, use default value in constructor
        if not num:
            num = self.genAmount

        # loop num times
        for _ in range(num):
            for i in range(self.numProcesses):
                strInst = ""
                listInst = []
                # loop instruction length times for single,double, or triple length
                for _ in range(self.instLength[0]):
                    self.shuffleChoices()

                    privileged = self.privelegedChances[0]
                    sleeping = self.sleepChances[0]
                    itype = self.choices[0]
                    r1, r2 = self.registers[:2]
                    if self.keepInstLocal:
                        if not privileged:
                            mb1 = self.memblocks[0]
                            mb2 = self.memblocks[0]
                        else:
                            mb1 = mb2 = "P"
                    else:
                        if not privileged:
                            mb1, mb2 = self.memblocks[:2]
                        else:
                            mb1 = "P"
                            mb2 = self.memblocks[0]

                    madd1, madd2 = self.memaddress[:2]

                    listInst.append(f"READ {mb1}{madd1} {r1}")
                    listInst.append(f"READ {mb2}{madd2} {r2}")
                    listInst.append(f"{itype} {r1} {r2}")
                    listInst.append(f"WRITE {mb1}{madd1} {r1}")
                    if privileged:
                        listInst.append(f"LOAD {i} R3")
                        listInst.append(f"LOAD {pCount} R4")
                        pCount += 1

                self.processInstructions[i].append(listInst)
                if sleeping:
                    a, b = self.sleepRange
                    self.processInstructions[i].append([f"sleep {randint(a,b)}"])

        for i in range(self.numProcesses):
            with open(self.outFilePattern + str(i) + ".exe", "w") as f:
                json.dump(self.processInstructions[i], f, indent=3)
        return json.dumps(self.processInstructions, indent=3)

    def getJson(self, pid=None):
        if not pid:
            return json.dumps(self.processInstructions, indent=3)
        else:
            if pid in self.processInstructions:
                return json.dumps(self.processInstructions[pid], indent=3)

        return None

    def __str__(self):
        inst = {}
        inst["inst"] = self.processInstructions
        inst["processes"] = len(inst["inst"])
        inst["instCount"] = 0
        for sec in inst["inst"]:
            for i in inst["inst"][sec]:
                inst["instCount"] += 1
        return json.dumps(inst, indent=2)

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    ri = RandInstructions(privilegedRatio=0.3, sleepRatio=0.15, numProcesses=5)

    print(ri)
