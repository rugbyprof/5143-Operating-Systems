Creating an auto code generator for your operating systems class project sounds like a great idea! To achieve this, you can develop a script that randomly generates sequences of instructions based on the constraints and requirements you've mentioned. Here's a high-level approach to creating such a generator:

1. **Define Constants and Constraints:**
   Define the constraints of your system, such as the number of available registers, the maximum addressable memory size, and the range of valid values for operands and addresses.

2. **Instruction Set Definition:**
   Create a dictionary or set of valid instructions along with their possible operand formats. For example:
   ```python
   instruction_set = {
       "LOAD": ["R", "M"],
       "STORE": ["R", "M"],
       "ADD": ["R", "R", "M"],
       # ... Define other instructions and their operand formats
   }
   ```

3. **Memory Allocation:**
   Randomly allocate memory locations for storing data and instructions for each executable file. The memory size for each file can vary within a specified range.

4. **Instruction Generation:**
   Generate sequences of instructions for each executable. Ensure that you follow the logic you mentioned, where instructions assume that all necessary previous instructions have been executed. Here's a simplified example of instruction generation in Python:

   ```python
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
   ```

5. **Validation:**
   To ensure correctness, you can develop a separate script that simulates the execution of the generated instructions. This simulator can maintain registers and memory state, execute instructions sequentially, and check if each instruction is logically valid given the assumed preconditions.

6. **Refinement and Testing:**
   Continuously refine and test your auto code generator and simulator. You might need to adjust the probabilities of different instruction types to achieve desired instruction mixes.

Remember that this is a simplified outline, and you can expand and customize it to suit your needs. Additionally, error handling and corner cases (such as division by zero) should be considered in both the generator and simulator.