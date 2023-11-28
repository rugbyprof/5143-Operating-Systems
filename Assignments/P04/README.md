## P04 - Distributed Instructions Simulation
#### Due: 12-11-2023 (Week of Dec 11<sup>th</sup>)

# Last Rewrite
# NOT DONE!! THIS WILL LEAVE WHEN DONE!!!

## Overview

This last version of P04 will not require the use of a complex class structure for you to implement. That doesn't mean that you cannot implement these classes to solve the overall problem, but I will not require it. So let me summarize what the problem will be. Look at the animated gif below: 

### Grayscale
<img src="https://images2.imgbox.com/02/d5/l6AecCY1_o.gif" width="400">

### Invert
<img src="https://images2.imgbox.com/11/7a/CMidzv13_o.gif" width="400">

This shows a couple of examples of my "distributed instruction execution" idea. Imagine that each of these 100x100 blocks are being `grayscaled` or `inverted` by different nodes on a computer network. By using rabbitmq for message passing, each group can work on a different portion of the image. 

## Example Code Chunks

Below are examples of the assembly code you will receive and must "execute" (evaluate) to obtain a value in which to send back to the "head node". The instructions will be in hexadecimal format, but it shouldn't be hard to convert between hex -> binary -> assembly :) 

#### Inverting a Pixel
This code is the assembly code that you will receive from the the "head node". The example below is equivalent to a single instruction, however, you will get many times this number (100x100 for example) of instructions. 


```ass
[
    'load r1 814',
    'load r2 591',
    'load r3 255',
    'load r4 73',
    'load r5 118',
    'load r6 35',
    'sub r4 r3',
    'sub r5 r3',
    'sub r6 r3',
    'store (r4,r5,r6) (r1,r2)',
]
```
Where the last store command will be converted to a message and sent to rabbitmq with (in this instance) `{"store":[182,137,220],"xy":[814,591]}`



#### Grayscaling a Pixel
Here is an example assembly instruction for gray scaling a pixel.
```
[
    'load r1 406',
    'load r2 230',
    'load r3 220',
    'load r4 72',
    'load r5 10',
    'load r6 3',
    'add r3 r4',
    'add r3 r5',
    'div r3 r6',
    'store (r3,r3,r3),(r1,r2)',
]
```
Where the last store command will be converted to a message and sent to rabbitmq with (in this instance) `{"store":[100,100,100],"xy":[406,230]}`

Basically, whenever you see a "store" instruction, you will message the "head" node with this exact syntax no matter the image manipulation function we are working with: 

```
{"store":[r,g,b],"xy":[x,y]}
```

Where:
- r = red channel 
- g = green channel 
- b = blue channel 
- x = x coordinate
- y = y coordinate

Basically I should be able to send you any `pseudo assembly` instruction in the above format, and you will send back an answer in the form of a new RGB value, and which XY coordinate to store it. 


## Old Design Approach

You don't need to implement all of these classes, but some of them actually may help you organize your implementation. 

### 1. ~~CPU Class~~
The CPU class is the central class that composes the other components. It should manage the overall operation, like executing instructions, managing data flow between components, etc.

### 2. ~~Registers Class~~
This class represents the CPU's register set. Each register can hold a value and has a unique identifier. The number of registers can be a fixed size, depending on the complexity you want to simulate.

### 3. ~~ALU Class~~
The ALU is responsible for arithmetic and logical operations. It takes inputs from the registers, performs operations, and writes the results back to the registers or memory.

### 4. ~~Cache Class~~
The cache simulates the CPU's internal cache, storing data that's frequently accessed or recently used. This can be a simplified version to demonstrate the concept of caching.

### Example Implementation
Here's a skeleton implementation in Python:

```python
class RegisterSet:
    def __init__(self, size=8):
        self.registers = [0] * size

    def read(self, reg_num):
        return self.registers[reg_num]

    def write(self, reg_num, value):
        self.registers[reg_num] = value

class ALU:
    def execute(self, operation, operand1, operand2):
        # Implement basic operations like add, subtract, etc.
        if operation == "add":
            return operand1 + operand2
        # ... other operations ...

class Cache:
    def __init__(self, size=64):
        self.cache = [None] * size
        # Simple cache implementation

class CPU:
    def __init__(self):
        self.registers = RegisterSet()
        self.alu = ALU()
        self.cache = Cache()

    def execute_instruction(self, instruction):
        # Decode instruction and perform actions
        # For example, an instruction to add two numbers
        operand1 = self.registers.read(1)  # Example
        operand2 = self.registers.read(2)  # Example
        result = self.alu.execute("add", operand1, operand2)
        self.registers.write(3, result)  # Store result in a register

# Example usage
cpu = CPU()
cpu.execute_instruction(...)
```

### Notes
- **Modularity**: Each component is a separate class, promoting modularity and separation of concerns.
- **Scalability**: This basic structure allows you to scale the complexity of each component according to the educational goals.

Regarding singletons like the system clock: yes, they can be suitable for elements that are truly singular in a system (like a clock). However, for components that can have multiple instances in different contexts (like CPUs in a multi-core system), it's better to use regular instances.


### Hex To Instruction

To streamline an arithmetic expression into pseudo-assembly, and then into binary for processing by the ALU, we can approach this in a few steps. Here's an outline of the process:

1. **Parse the Arithmetic Expression**: Break down the arithmetic expression into its constituent parts (operands and operators).

2. **Convert to Pseudo-Assembly**: Translate the parsed expression into a series of pseudo-assembly instructions.

3. **Convert to Binary**: Transform the pseudo-assembly into binary code based on your specified opcodes and register binary representations.

4. **Load and Execute in CPU**: The CPU will then process these binary instructions, using the cache and registers, and the ALU will perform the necessary arithmetic operations.

### Example Implementation

Let's create a few helper classes and functions to demonstrate this process:

1. **Expression Parser**:

```python
def parse_expression(expression):
    # This function will parse the expression '3 + 4 - 7' into ['3', '+', '4', '-', '7']
    return [part.strip() for part in expression.split()]
```

2. **Pseudo-Assembly Converter**:

```python
def expression_to_assembly(expression):
    operators = {"+": "ADD", "-": "SUB", "*": "MUL", "/": "DIV", "%": "MOD"}
    parsed_expression = parse_expression(expression)
    assembly_code = []
    register_counter = 1

    for i, part in enumerate(parsed_expression):
        if part.isdigit():
            assembly_code.append(f'LOAD R{register_counter} {part}')
            register_counter += 1
        elif part in operators:
            op1 = f'R{register_counter-2}'
            op2 = f'R{register_counter-1}'
            assembly_code.append(f'{operators[part]} R{register_counter} {op1} {op2}')
            register_counter += 1

    return assembly_code
```

3. **Binary Converter**:

```python
def assembly_to_binary(assembly_code):
    opcodes = {
        "LOAD": "1010",
        "ADD": "1011",
        "SUB": "1100",
        "MUL": "1101",
        "DIV": "1110",
        "MOD": "1111",
    }
    binary_code = []

    for line in assembly_code:
        parts = line.split()
        opcode = opcodes[parts[0]]
        operands = ' '.join(format(int(x[1:]), '04b') for x in parts[1:])
        binary_code.append(f'{opcode} {operands}')

    return binary_code
```

4. **Putting It All Together**:

```python
expression = "3 + 4 - 7"
assembly = expression_to_assembly(expression)
binary = assembly_to_binary(assembly)

print("Pseudo-Assembly:")
print("\n".join(assembly))

print("\nBinary Code:")
print("\n".join(binary))

# This binary code can be then processed by the CPU class, going through RAM and cache, and executed by the ALU.
```



-----

Determining the number of operands and operators in an arithmetic expression, especially when dealing with varying lengths and complexities, requires a more robust parsing strategy. In the context of converting an expression to pseudo-assembly and then to binary, accurately identifying operands (numbers) and operators (+, -, *, etc.) is crucial for correct instruction generation.

### Strategy for Parsing Expressions:

1. **Tokenization**: Break the expression into tokens (operands and operators).

2. **Counting Operands and Operators**: Count the number of operands and operators as they are parsed.

3. **Handling Different Lengths**: Ensure the parser can handle expressions of varying lengths and complexities.

### Example Implementation:

Let's improve the parsing function to handle expressions with different numbers of operands and operators:

```python
def parse_expression(expression):
    # Tokenize the expression into operands and operators
    tokens = expression.split()
    operands = [token for token in tokens if token.isdigit()]
    operators = [token for token in tokens if not token.isdigit()]
    return operands, operators
```

This function splits the expression into tokens and then separates operands (numbers) from operators (arithmetic symbols).

### Applying the Parsing Strategy:

Here's how you would use this improved parsing strategy in the overall process:

```python
expression = "3 + 4 - 7 * 2 / 5"

# Parse the expression
operands, operators = parse_expression(expression)

# Information about the expression
print(f"Operands: {operands} (Count: {len(operands)})")
print(f"Operators: {operators} (Count: {len(operators)})")

# Further processing (conversion to assembly, binary, etc.)
# ...
```

### Considerations:

- **Complex Expressions**: For more complex expressions (e.g., those with parentheses, precedence rules), a more sophisticated parsing algorithm, like the shunting-yard algorithm, might be necessary.
- **Assembly and Binary Conversion**: The methods for converting to pseudo-assembly and binary will also need to accommodate the variability in the number of operands and operators. This might involve more complex logic to handle different scenarios and ensure correct register allocation and operation sequencing.

This approach provides a flexible and robust way to dissect arithmetic expressions of varying complexities, which is a critical step in translating them into machine-understandable code.


------

If we're assuming a 4-bit chunk size to parse binary code and using '\n' as the delimiter for separate expressions, we need to adjust our parsing strategy. This approach aligns well with binary instruction sets, where each instruction, operator, or operand is represented as a fixed-length binary string.

### Strategy for 4-bit Binary Parsing:

1. **Chunk Parsing**: Split the expression into 4-bit chunks.

2. **Expression Delimitation**: Use '\n' to separate different expressions.

3. **Identifying Instructions, Operators, and Operands**: Map the 4-bit binary chunks to their corresponding instructions, operators, or operands.

### Example Implementation:

Let's assume we have a string of binary code where each 4-bit chunk represents either an instruction, an operator, or an operand. Each expression is separated by a newline character '\n'.

```python
def parse_binary_expression(binary_expression):
    # Splitting expressions by newline
    expressions = binary_expression.strip().split('\n')

    parsed_expressions = []
    for expression in expressions:
        # Splitting the expression into 4-bit chunks
        chunks = [expression[i:i+4] for i in range(0, len(expression), 4)]

        # Mapping each chunk to its meaning (this part is dependent on your mapping)
        mapped_chunks = [binary_to_instruction(chunk) for chunk in chunks]

        parsed_expressions.append(mapped_chunks)

    return parsed_expressions

def binary_to_instruction(chunk):
    # Example mapping, should be replaced with actual mapping
    mapping = {
        "0001": "LOAD",
        "0010": "ADD",
        "0011": "SUB",
        # Add mappings for all 16 possible 4-bit values
    }
    return mapping.get(chunk, "UNKNOWN")
```

### Example Usage:

For the sake of demonstration, let's use a simplified binary string with each expression separated by '\n':

```python
binary_code = "000100110010\n001000110011"

parsed_expressions = parse_binary_expression(binary_code)

for expression in parsed_expressions:
    print("Parsed Expression:", expression)
```

This script will parse each 4-bit chunk of the binary string into its corresponding instruction or operand based on the provided mapping. It treats each line as a separate expression, allowing for multiple expressions to be parsed from a single input string.

### Considerations:

- **Mapping Accuracy**: The `binary_to_instruction` function must accurately map each 4-bit chunk to the correct instruction, operator, or operand. This mapping depends on your specific instruction set.
- **Error Handling**: You might want to include error handling for cases where a 4-bit chunk doesn't match any known instruction or operand.
- **Expression Complexity**: This method works well for linear expressions without nested or complex operations. For more complex instruction sets or operations, additional parsing logic may be needed.