from random import shuffle
from random import seed
from random import randint
import json
from rich import print
import sys
from registers import Registers

from rwLock import *

mem = None
with open("memory.json") as f:
    mem = json.load(f)

registers = Registers(2)


def writer():
    ans = 0
    instructions = []
    with open("writer_1.exe") as f:
        instructions = json.load(f)

    for insts in instructions:
        # acquire
        for inst in insts:

            i, loc, reg = inst.split()

            # print(f"{inst} {loc} {reg} ")
            # breaking up inst
            memBlock = loc[0]
            memAddr = loc[1:]
            register = int(reg[1]) - 1

            # print(f"{memBlock} {memAddr}")

            # loads registers
            if i == "READ":
                print("read")
                registers[register] = mem[memBlock][memAddr]

                if registers[register] is None:
                    registers[register] = randint(1, 9)

            if i in ["ADD", "SUB", "MUL", "DIV"]:
                print("arithmetic")
                registers[0] = OPS[i](registers[0], registers[1])

            if i == "WRITE":
                print("write")
                mem[memBlock][memAddr] = registers[0]
        # release
    print(mem)


if __name__ == "__main__":

    w = writer()

    # seed(25256)

    # if len(sys.argv) == 1:
    #     writers = 1

    # else:
    #     writers = int(sys.argv[1])

    # readers = int(writers) * 3

    # rw_lock = RWLock()
    # threads = []

    # for i in range(writers):
    #     threads.append(Writer(rw_lock, 1, 0, i))

    # for i in range(readers):
    #     threads.append(Reader(rw_lock, 0.1, 0.3))

    # shuffle(threads)

    # buffer_, rw_lock, init_sleep_time, sleep_time, to_write
    # threads.append(Reader(rw_lock, 0.1, 0.6))
    # threads.append(Writer(rw_lock, 0.2, 0.1, 2))
    # threads.append(Reader(rw_lock, 0.3, 0))
    # threads.append(Reader(rw_lock, 0.4, 0))
    # threads.append(Writer(rw_lock, 0.5, 0.1, 3))

    # for t in threads:
    #     t.run()

    # print(threads)

    # print(buffer)
