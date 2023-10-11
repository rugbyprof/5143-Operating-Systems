class ImageProcessor:
    def __init__(self, image_width, image_height, image_data):
        self.image_width = image_width
        self.image_height = image_height
        self.image_data = image_data

    def load(self, register, mem_addr):
        return self.image_data[mem_addr]

    def add(self, register1, register2, register3):
        return register2 + register3

    def sub(self, register1, register2, register3):
        return register2 - register3

    def max(self, register1, register2, value):
        return max(register2, value)

    def min(self, register1, register2, value):
        return min(register2, value)

    def store(self, register, mem_addr, value):
        self.image_data[mem_addr] = value

    def execute_pseudo_assembly(self, pseudo_assembly_code):
        # Split the pseudo-assembly code into lines
        instructions = pseudo_assembly_code.split('\n')

        # Initialize registers and memory address
        registers = {'R1': 0, 'R2': 0, 'R3': 0, 'R4': 0, 'R5': 0, 'R6': 0}
        mem_addr = 0

        for instruction in instructions:
            parts = instruction.split()

            if not parts:
                continue

            opcode = parts[0]

            if opcode == 'LOAD':
                register = parts[1][:-1]  # Remove the comma
                mem_addr = int(parts[2])
                registers[register] = self.load(register, mem_addr)

            elif opcode == 'ADD':
                register1 = parts[1][:-1]  # Remove the comma
                register2 = parts[2][:-1]
                register3 = parts[3]
                registers[register1] = self.add(register1, registers[register2], registers[register3])

            elif opcode == 'SUB':
                register1 = parts[1][:-1]
                register2 = parts[2][:-1]
                register3 = parts[3]
                registers[register1] = self.sub(register1, registers[register2], registers[register3])

            elif opcode == 'MAX':
                register1 = parts[1][:-1]
                register2 = parts[2][:-1]
                value = int(parts[3])
                registers[register1] = self.max(register1, registers[register2], value)

            elif opcode == 'MIN':
                register1 = parts[1][:-1]
                register2 = parts[2][:-1]
                value = int(parts[3])
                registers[register1] = self.min(register1, registers[register2], value)

            elif opcode == 'STORE':
                register = parts[1][:-1]
                mem_addr = int(parts[2])
                value = registers[register]
                self.store(register, mem_addr, value)

        return self.image_data
