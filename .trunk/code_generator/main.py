


instruction_set = {
    "LOAD": ["R", "M"],
    "STORE": ["R", "M"],
    "ADD": ["R", "R", "R"],
    # ... Define other instructions and their operand formats
}



import random

def generate_instruction():
    instruction = random.choice(list(instruction_set.keys()))
    operands = []
    for format in instruction_set[instruction]:
        if format == "R":
            operands.append("R" + str(random.randint(0, num_registers - 1)))
        elif format == "M":
            operands.append("M" + str(random.randint(0, max_memory_address)))
        # Add other operand formats here
    return f"{instruction} {' '.join(operands)}"

def generate_executable(num_instructions):
    instructions = []
    for _ in range(num_instructions):
        instructions.append(generate_instruction())
    return instructions

# Example usage
num_registers = 4
max_memory_address = 255
num_instructions = 50
executable = generate_executable(num_instructions)
for instruction in executable:
    print(instruction)
