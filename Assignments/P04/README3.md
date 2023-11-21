## P04 - Distributed Instructions Simulation
#### Due: 12-11-2023 (Week of Dec 11<sup>th</sup>)



## Overview

This project has to do with you or your group writing a slave node that will run instructions received from a main or master node. We can picture the setup as a cluster of nodes all working on the same instructions as delivered by the message server. I have mentioned many times that I wanted to keep this simple by not implememting `cache` or `ram`, but I think it would actually make the division of labor easier by adding these two items. 

<img src="https://images2.imgbox.com/5a/1c/wlHSXkEv_o.png" width="600">

If you look at the graphic above, you can see what I perceive, visually, as the data flow. Let me list it out in laymens terms.

1. Message Server sends messages to your "node".
2. The `Node` class will be in charge of listening for incoming messages, will place them on an `unbounded queue`.
3. If they fit into Ram, then a block of messages (instructions) will get copied into ram. No real addressing, just serial address locations.
4. The `Cpu` class, which is in charge of `fetching`, `decoding`, and `executing` instructions will do so. 
   - A `Fetch` copies a block of instructions in cache.
   - `Decode` turns it from `Hex` into `Binary`.
   - `Execute` does just that with the `ALU`
5. After an instruction is executed, we need to 
### CPU Class
The `CPU` class will be the central orchestrator. It should handle the following:

- **Fetch**: Retrieve instruction blocks from a queue or buffer.
- **Decode**: Interpret each instruction (perhaps a separate `Decoder` class or function could be useful).
- **Execute**: Pass the decoded instruction to the appropriate handler (`ALU`, `Registers`, etc.).
- **Control Logic**: Manage instruction flow, determining the order of execution and handling branching, if any.
- **Communication Interface**: Methods to receive instruction blocks and send back results.


```python
class CPU:
    def __init__(self):
        self.alu = ALU()
        self.registers = Registers()
        # Initialize other components as needed

    def fetch(self, instruction_block):
        # Fetch instructions
        pass

    def decode(self, instruction):
        # Decode an instruction
        pass

    def execute(self, instruction):
        # Execute an instruction
        pass

    def run(self, instruction_block):
        for instruction in instruction_block:
            decoded_instruction = self.decode(instruction)
            self.execute(decoded_instruction)

```

### ALU Class

- The `ALU` is responsible for all arithmetic and logical operations.
- Our ALU is only responsible for "executing" the arithmetic. 
- The cpu will "decode" the instruction first. 

```python
class ALU:
    def __init__(self, registers):
        """
        Initialize the ALU with a reference to the Registers object.

        :param registers: A reference to the Registers object for reading and writing register values.
        """
        self.registers = registers
        self.operations = {
            'ADD': self._add,
            'SUB': self._sub,
            'MUL': self._mul,
            'DIV': self._div,
            'MOD': self._mod
        }

    def execute(self, operation, dest, src1, src2):
        """
        Execute the specified arithmetic operation.

        :param operation: The arithmetic operation to perform ('ADD', 'SUB', etc.).
        :param dest: Destination register.
        :param src1: First source register.
        :param src2: Second source register.
        """
        if operation in self.operations:
            self.operations[operation](dest, src1, src2)
        else:
            raise ValueError(f"Unknown operation: {operation}")

    def _add(self, dest, src1, src2):
        # Implementation for addition

    def _sub(self, dest, src1, src2):
        # Implementation for subtraction

    def _mul(self, dest, src1, src2):
        # Implementation for multiplication

    def _div(self, dest, src1, src2):
        # Implementation for division

    def _mod(self, dest, src1, src2):
        # Implementation for modulo
```

### Register Class:

Below are a list of possible attributes that you could see in a more realistic simulation. For our simulation, we only need 2-3 of the attributes listed.

1. **Name or Identifier**: A unique identifier or name for the register, like `R1`, `R2`, etc. This is useful for referencing and debugging.

2. **Type** (optional not necessary): Differentiate between types of registers (e.g., general-purpose, special-purpose like instruction pointer, stack pointer, etc.).

3. **Status Flags** (optional not necessary): Include flags to indicate certain conditions after operations (e.g., zero flag, overflow flag, negative flag). This might be more relevant at the CPU level but can be considered for complex simulations.

4. **Lock or Busy Flag**: Indicates if the register is currently in use or locked during multi-threaded or parallel operations.

5. **Timestamp or Last Accessed** (optional not necessary): Store the last time the register was accessed or modified, which can be useful for debugging or for certain cache algorithms.

6. **Access Count** (optional not necessary): Count how many times the register has been accessed or written to. This could be valuable for performance analysis or certain scheduling algorithms.

7. **Size**: Information about the size of the register (like 32-bit, 64-bit). This helps in ensuring that operations respect the boundaries of the register size.

8. **Default Value**: A default or initial value for the register, which can be used to reset or initialize it.

9. **Read-Only Flag** (optional not necessary): A flag to indicate if the register is read-only. This is useful for simulating special registers that cannot be modified directly by instructions.

10. **Metadata** (optional not necessary): Any additional metadata relevant to your simulation, like the register's role or special characteristics.

Here's a simple Python skeleton for such a class:

```python
class Register:
    def __init__(self, name, reg_type='general', size=32):
        self.name = name
        self.reg_type = reg_type
        self.value = 0  # Default value
        self.size = size
        self.locked = False
        self.last_accessed = None
        self.access_count = 0
        self.read_only = False

    # Additional methods for setting, getting, locking, etc.
```

You can expanded the class with methods for setting and getting the value, locking and unlocking the register, and other functionalities as needed. 

### Registers:

The `Registers` class will act as a container and manager for multiple `Register` objects.

```python
class Registers:
    def __init__(self, num_registers):
        """
        Initialize the Registers container with a specified number of registers.

        :param num_registers: The number of registers to create.
        """
        self.registers = {}  # Dictionary to store Register objects, keyed by their names or identifiers.
        self.num_registers = num_registers  # Total number of registers in this container.

        # Initialize the registers here
        # for i in range(num_registers):
        #     self.registers[f'R{i}'] = Register(f'R{i}')

    # Attributes

    # self.registers: dict
    #     Stores individual Register objects. Provides easy access to each register by its name or ID.

    # self.num_registers: int
    #     The total number of registers in the container. This is set during initialization and is used to
    #     create the correct number of Register objects.

    # Methods (to be implemented)
    # - Method to read a value from a specific register.
    # - Method to write a value to a specific register.
    # - Method to reset all registers to their default state.
    # - Method to lock or unlock a specific register (for multi-threading scenarios).
    # - Method to get the status of a specific register (like if it's locked, its last accessed time, etc.).
    # - Additional methods as required for your simulation's needs.
```


### Ram Class
The `Ram` class will store instruction blocks, each containing a fixed number of instructions. Given that each instruction is 12 bits and a block contains 10 instructions, each block will be 120 bits.

#### Attributes and Function Headers

```python
class Ram:
    def __init__(self, size):
        """
        Initialize RAM with a given size.

        :param size: Total size of RAM, which determines how many blocks it can store.
        """
        self.memory = {}  # Dictionary to store instruction blocks, keyed by block address.
        self.block_size = 10  # Number of instructions per block.
        self.instruction_size = 12  # Size of each instruction in bits.
        self.size = size  # Total size of RAM.

    def store_block(self, address, block):
        """
        Store a block of instructions at a specified address.

        :param address: The address where the block will be stored.
        :param block: The block of instructions to store.
        """

    def retrieve_block(self, address):
        """
        Retrieve a block of instructions from a specified address.

        :param address: The address of the block to retrieve.
        """
```

#### Addressing Scheme
- **Block Addressing**: Each address in RAM corresponds to the start of a block of instructions.
- **Sequential Addressing**: Addresses could be sequential, representing each block (e.g., 0, 1, 2, ...).

### Cache Class
The `Cache` class will request and store blocks of instructions from the `Ram` class for faster access.

#### Attributes and Function Headers

```python
class Cache:
    def __init__(self, ram, cache_size):
        """
        Initialize Cache with a reference to the RAM and a specified size.

        :param ram: A reference to the Ram object.
        :param cache_size: The number of blocks the cache can store.
        """
        self.ram = ram  # Reference to the RAM object.
        self.cache = {}  # Dictionary to store cached blocks, keyed by block address.
        self.cache_size = cache_size  # Number of blocks the cache can store.

    def load_block(self, address):
        """
        Load a block from RAM into the cache. If the cache is full, apply a cache eviction policy.

        :param address: The address of the block in RAM to load into the cache.
        """

    def get_instruction(self, address, instruction_index):
        """
        Get a specific instruction from a block in the cache.

        :param address: The address of the block in the cache.
        :param instruction_index: The index of the instruction within the block (0-9).
        """
```

#### Addressing Scheme and Cache Mechanics
- **Cache Eviction Policy**: Implement a simple policy like Least Recently Used (LRU) or First-In-First-Out (FIFO) for cache eviction when it's full.
- **Partial Block Loading**: Optionally, consider mechanisms to load only parts of a block if your simulation requires it.

