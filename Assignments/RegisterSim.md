## Project X - Register Simulation / Virtualization
#### Due: TBD


To implement the `registers` portion of the simulation, you can break it down into different types of registers and describe their functions and usage. Here's a breakdown of the registers commonly found in a CPU simulation:

1. **Instruction Register (IR):**
   - Function: Stores the current instruction being executed.
   - Usage: Fetches the instruction from memory and holds it for decoding and execution by the CPU.
   - Pseudo code implementation:
     ```c++
     IR = FetchInstruction()  // Fetch instruction from memory
     ```

2. **Program Counter (PC):**
   - Function: Stores the memory address of the next instruction to be fetched.
   - Usage: Determines the location of the next instruction to fetch.
   - Pseudo code implementation:
     ```c++
     PC = InitialMemoryAddress  // Set PC to the initial memory address

     // In the execution loop, increment PC after each instruction fetch
     PC = PC + InstructionSize
     ```

3. **Accumulator (AC):**
   - Function: Stores intermediate results of arithmetic and logical operations.
   - Usage: Holds the result of arithmetic operations and serves as a temporary storage during computations.
   - Pseudo code implementation:
     ```c++
     AC = 0  // Initialize the accumulator to 0

     // Example arithmetic operation: Addition
     AC = AC + Value
     ```

4. **General-Purpose Registers (GPR):**
   - Function: Provides additional storage for data and calculations.
   - Usage: Holds data during computations, function call parameters, and return values.
   - Pseudo code implementation:
     ```c++
     GPR1 = Value1  // Store a value in a general-purpose register
     Result = GPR2  // Retrieve a value from a general-purpose register
     ```

It's important to note that the number and purpose of registers can vary depending on the CPU architecture. You can adjust the register set based on your specific requirements or the architecture you're simulating.

In pseudo code, you can represent the set of registers using variables or an array, depending on your preference. Here's an example of implementing the registers using an array in pseudo code:

```c++
// Initialize registers
IR = 0
PC = InitialMemoryAddress
AC = 0
GPR = [0, 0, 0, 0]  // Assuming 4 general-purpose registers

// Example usage
IR = FetchInstruction()  // Fetch instruction from memory
PC = PC + InstructionSize

AC = AC + GPR[1]  // Perform addition using the accumulator and a general-purpose register
GPR[3] = AC  // Store the accumulator value in a general-purpose register
```

Remember to adapt the implementation based on the programming language you are using for your simulation.