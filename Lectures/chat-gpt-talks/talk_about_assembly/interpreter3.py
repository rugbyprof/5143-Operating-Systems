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
    def __init__(self):
        self.registers = {}

    def loadAddr(self, register, mem_addr):
        # Simulated loading from memory address mem_addr into register
        self.registers[register] = mem_addr  # Load the data into the register

    def loadVal(self, register, mem_addr):
        # Simulated loading from memory address mem_addr into register
        self.registers[register] = self.memory[mem_addr]  # Load the actual data into the register



    def add(self, register1, register2, register3):
        # Simulated addition of register2 and register3, storing the result in register1
        self.registers[register1] = self.registers[register2] + self.registers[register3]

    def sub(self, register1, register2, register3):
        # Simulated subtraction of register3 from register2, storing the result in register1
        self.registers[register1] = self.registers[register2] - self.registers[register3]

    def mul(self, register1, register2, register3):
        # Simulated multiplication of register2 and register3, storing the result in register1
        self.registers[register1] = self.registers[register2] * self.registers[register3]

    def div(self, register1, register2, register3):
        # Simulated division of register2 by register3, storing the result in register1
        if self.registers[register3] != 0:
            self.registers[register1] = self.registers[register2] / self.registers[register3]
        else:
            self.registers[register1] = 0  # Avoid division by zero

    def max(self, register1, register2, value):
        # Simulated maximum between register2 and a value, storing the result in register1
        self.registers[register1] = max(self.registers[register2], value)

    def min(self, register1, register2, value):
        # Simulated minimum between register2 and a value, storing the result in register1
        self.registers[register1] = min(self.registers[register2], value)

    def store(self, register, mem_addr):
        # Simulated storing the value in the register to a memory address mem_addr
        # This can be customized based on your specific needs
        pass

    def execute_pseudo_assembly(self, pseudo_assembly_code):
        # Split the pseudo-assembly code into lines
        instructions = pseudo_assembly_code.split('\n')

        # Initialize registers
        self.registers = {}

        for instruction in instructions:
            parts = instruction.split()

            if not parts:
                continue

            opcode = parts[0]

            if opcode == 'LOAD':
                register = parts[1][:-1]  # Remove the comma
                mem_addr = int(parts[2])
                self.registers[register] = self.load(register, mem_addr)

            elif opcode in ('ADD', 'SUB', 'MUL', 'DIV'):
                register1 = parts[1][:-1]  # Remove the comma
                register2 = parts[2][:-1]
                register3 = parts[3]
                getattr(self, opcode.lower())(register1, register2, register3)

            elif opcode in ('MAX', 'MIN'):
                register1 = parts[1][:-1]
                register2 = parts[2][:-1]
                value = int(parts[3])
                getattr(self, opcode.lower())(register1, register2, value)

            elif opcode == 'STORE':
                register = parts[1][:-1]
                mem_addr = int(parts[2])
                self.store(register, mem_addr)

        return self.registers
