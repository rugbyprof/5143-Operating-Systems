from random import shuffle
import json
import random
from datetime import datetime


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
        print(self.seed)
        random.seed(self.seed)

        # pull possible params from kwargs to tailor the building of
        # instructions
        self.addressRange = kwargs.get("addressRange", (100, 255, 5))
        self.choices = kwargs.get("choices", ["ADD", "SUB", "MUL", "DIV"])
        self.genAmount = kwargs.get("genAmount", 100)
        self.memblocks = kwargs.get("memblocks", ["A", "B", "C"])
        self.registers = kwargs.get("registers", ["R1", "R2"])
        self.retFormat = kwargs.get("retFormat", "json")  # or 'str'
        self.outFile = kwargs.get("outFile", "program.exe")
        self.keepInstLocal = kwargs.get("keepInstLocal", False)
        self.privileged = kwargs.get("privileged", 0)

        print(self.privileged)
        self.privelegedChances = [0]

        if self.privileged > 0:
            self.privelegedChances = []
            ptrue = int(self.privileged * 100)
            pfalse = 100 - ptrue
            for _ in range(ptrue):
                self.privelegedChances.append(1)
            for _ in range(pfalse):
                self.privelegedChances.append(0)

        print(self.privelegedChances)

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

    def generateInstructions(self, num=None):
        """
        Params:
            num (int) : number of instructions to generate
        """
        # no num passed in, use default value in constructor
        if not num:
            num = self.genAmount

        # loop num times
        for _ in range(num):
            strInst = ""
            listInst = []
            # loop instruction length times for single,double, or triple length
            for _ in range(self.instLength[0]):
                self.shuffleChoices()

                privileged = self.privelegedChances[0]
                itype = self.choices[0]
                r1, r2 = self.registers[:2]
                if self.keepInstLocal:
                    if not privileged:
                        mb1 = mb2 = self.memblocks[:1]
                    else:
                        mb1 = mb2 = "P"
                else:
                    if not privileged:
                        mb1, mb2 = self.memblocks[:2]
                    else:
                        mb1 = "P"
                        mb2 = self.memblocks[:1]

                madd1, madd2 = self.memaddress[:2]

                strInst += f"READ {mb1}{madd1} {r1}\n"
                strInst += f"READ {mb2}{madd2} {r2}\n"
                strInst += f"{itype} {r1} {r2}\n"
                strInst += f"WRITE {r1} {mb1}{madd1}\n"

                listInst.append(f"READ {mb1}{madd1} {r1}")
                listInst.append(f"READ {mb2}{madd2} {r2}")
                listInst.append(f"{itype} {r1} {r2}")
                listInst.append(f"WRITE {r1} {mb1}{madd1}")

            self.strInstructions += strInst
            self.listInstructions.append(listInst)

        if self.retFormat == "json":
            with open(self.outFile, "w") as f:
                json.dump(self.listInstructions, f, indent=3)
            return json.dumps(self.listInstructions, indent=3)
        else:
            with open(self.outFile, "w") as f:
                f.write(self.strInstructions)
            return self.strInstructions

    def getJson(self):
        return json.dumps(self.listInstructions, indent=3)

    def getStr(self):
        return self.strInstructions


if __name__ == "__main__":
    ri = RandInstructions(privileged=0.3)

    print(ri.getJson())
