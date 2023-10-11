class Interpreter:
    def __init__(self,data):
        self.data = data
        self.registers = {}

    def load(self, register, mem_addr):
        return self.data[mem_addr]

    def add(self, register1, register2, register3):
        return register2 + register3

    def sub(self, register1, register2, register3):
        return register2 - register3

    def mul(self, register1, register2, register3):
        return register2 * register3

    def div(self, register1, register2, register3):
        if register3 != 0:
            return register2 / register3
        else:
            return 0  # Avoid division by zero

    def max(self, register1, register2, value):
        return max(register2, value)

    def min(self, register1, register2, value):
        return min(register2, value)

    def store(self, register, mem_addr, value):
        self.data[mem_addr] = value

    def execute_pseudo_assembly(self, pseudo_assembly_code):
        # Split the pseudo-assembly code into lines
        instructions = pseudo_assembly_code.split('\n')

        # Initialize registers and memory address
        self.registers = {}
        mem_addr = 0

        for instruction in instructions:
            parts = instruction.split()

            if not parts:
                continue

            opcode = parts[0]

            if opcode == 'LOAD':
                register = parts[1][:-1]  # Remove the comma
                mem_addr = int(parts[2])
                self.registers[register] = self.load(register, mem_addr)

            elif opcode == 'ADD':
                register1 = parts[1][:-1]  # Remove the comma
                register2 = parts[2][:-1]
                register3 = parts[3]
                self.registers[register1] = self.add(register1, self.registers[register2], self.registers[register3])

            elif opcode == 'SUB':
                register1 = parts[1][:-1]
                register2 = parts[2][:-1]
                register3 = parts[3]
                self.registers[register1] = self.sub(register1, self.registers[register2], self.registers[register3])

            elif opcode == 'MUL':
                register1 = parts[1][:-1]
                register2 = parts[2][:-1]
                register3 = parts[3]
                self.registers[register1] = self.mul(register1, self.registers[register2], self.registers[register3])

            elif opcode == 'DIV':
                register1 = parts[1][:-1]
                register2 = parts[2][:-1]
                register3 = parts[3]
                self.registers[register1] = self.div(register1, self.registers[register2], self.registers[register3])

            elif opcode == 'MAX':
                register1 = parts[1][:-1]
                register2 = parts[2][:-1]
                value = int(parts[3])
                self.registers[register1] = self.max(register1, self.registers[register2], value)

            elif opcode == 'MIN':
                register1 = parts[1][:-1]
                register2 = parts[2][:-1]
                value = int(parts[3])
                self.registers[register1] = self.min(register1, self.registers[register2], value)

            elif opcode == 'STORE':
                register = parts[1][:-1]
                mem_addr = int(parts[2])
                value = self.registers[register]
                self.store(register, mem_addr, value)

        return self.data
