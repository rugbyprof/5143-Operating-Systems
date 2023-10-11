class Memory:
    def __init__(self, size):
        self.size = size
        self.memory = [0] * size  # Initialize memory with zeros

    def read(self, mem_addr):
        # Read data from memory at the specified memory address
        if 0 <= mem_addr < self.size:
            return self.memory[mem_addr]
        else:
            raise ValueError("Memory address out of bounds")

    def write(self, mem_addr, data):
        # Write data to memory at the specified memory address
        if 0 <= mem_addr < self.size:
            self.memory[mem_addr] = data
        else:
            raise ValueError("Memory address out of bounds")

    def dump(self):
        # Dump the contents of memory (for debugging purposes)
        return self.memory



class PseudoAssemblyInterpreter:
    def __init__(self, memory):
        self.registers = {}
        self.memory = memory
        self.pc = 0  # Program counter
        self.loop_stack = []  # Stack to keep track of loop positions

    def execute_pseudo_assembly(self, code):
        instructions = code.split('\n')
        while self.pc < len(instructions):
            instruction = instructions[self.pc].strip()
            if instruction:
                self.execute_instruction(instruction)

    def execute_instruction(self, instruction):
        parts = instruction.split()
        opcode = parts[0].upper()

        if opcode == 'LOAD':
            # Handle LOAD instruction
            register = int(parts[1][1:])  # Parse register number from R1, R2, ...
            mem_addr = int(parts[2])
            self.load(register, mem_addr)
        elif opcode == 'STORE':
            # Handle STORE instruction
            register = int(parts[1][1:])  # Parse register number from R1, R2, ...
            mem_addr = int(parts[2])
            self.store(register, mem_addr)
        elif opcode == 'ADD':
            # Handle ADD instruction
            register_dest = int(parts[1][1:])
            register_src1 = int(parts[2][1:])
            value = int(parts[3])
            self.add(register_dest, register_src1, value)
        elif opcode == 'DIV':
            # Handle DIV instruction
            register_dest = int(parts[1][1:])
            register_src1 = int(parts[2][1:])
            value = int(parts[3])
            self.divide(register_dest, register_src1, value)
        elif opcode == 'CMP':
            # Handle CMP instruction
            register_src1 = int(parts[1][1:])
            value = int(parts[2])
            self.compare(register_src1, value)
        elif opcode == 'JNE':
            # Handle JNE instruction (conditional jump)
            target_label = parts[1]
            if self.registers['CMP'] != 0:
                self.jump_to_label(target_label)
        elif opcode == 'LOOP_ROW':
            # Handle LOOP_ROW label (start of row loop)
            self.loop_stack.append(self.pc)  # Push the current PC to the stack
        elif opcode == 'LOOP_COL':
            # Handle LOOP_COL label (start of column loop)
            if not self.loop_stack:
                raise ValueError("LOOP_COL without LOOP_ROW")
            # Jump back to the start of the row loop
            self.pc = self.loop_stack[-1]
        else:
            raise ValueError(f"Unknown instruction: {opcode}")

        self.pc += 1  # Increment program counter after executing an instruction

    def load(self, register, mem_addr):
        # Simulated loading from memory address mem_addr into register
        self.registers[register] = self.memory.read(mem_addr)

    def store(self, register, mem_addr):
        # Simulated storing data from register into memory address mem_addr
        self.memory.write(mem_addr, self.registers[register])

    def add(self, register_dest, register_src1, value):
        # Simulated ADD operation
        self.registers[register_dest] = self.registers[register_src1] + value

    def divide(self, register_dest, register_src1, value):
        # Simulated DIV operation
        self.registers[register_dest] = self.registers[register_src1] // value

    def compare(self, register_src1, value):
        # Simulated CMP operation (compare)
        self.registers['CMP'] = self.registers[register_src1] - value

    def jump_to_label(self, label):
        # Simulated jump to a label in the code
        for idx, instruction in enumerate(instructions):
            if label in instruction:
                self.pc = idx
                break
