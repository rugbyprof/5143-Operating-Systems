from random import shuffle
from rich import print 


def randInstruction(asList = False):

    choices = ["ADD", "SUB", "MUL", "DIV"]
    registers = ["R1", "R2"]
    memblocks = ["A", "B", "C"]
    memaddress = [x for x in range(100, 255, 5)]

    shuffle(choices)
    shuffle(registers)
    shuffle(memblocks)
    shuffle(memaddress)

    itype = choices[0]
    r1, r2 = registers[:2]
    mb1, mb2 = memblocks[:2]
    madd1, madd2 = memaddress[:2]

    if not asList:
        inst = ""
        inst += f"READ {mb1}{madd1} {r1}\n"
        inst += f"READ {mb2}{madd2} {r2}\n"
        inst += f"{itype} {r1} {r2}\n"
        inst += f"WRITE {r1} {mb1}{madd1}\n"
    else:
        inst = []
        inst.append(f"READ {mb1}{madd1} {r1}")
        inst.append(f"READ {mb2}{madd2} {r2}")
        inst.append(f"{itype} {r1} {r2}")
        inst.append(f"WRITE {r1} {mb1}{madd1}")
    
    return inst


instructions = []
for i in range(100):
    instructions.append(randInstruction(True))

print(instructions)

# blocks = ['A','B','C']
# locations = [x for x in range(0,255,5)]

# for block in blocks:
#     for location in locations:
#         location = 74747


# inst = 'A205'

# block = inst[:1]
# loc = inst[1:]

# print(block)
# print(loc)



# memory[block][loc] = 34

# with open("program1") as f:
#     instructions = f.readlines()

# for inst in 