## Project X - CPU Simulation / Virtualization
#### Due: TBD


## ALU
## CACHE
## REGISTERS

Here's an example of a basic simulated machine language with a few instruction types:

1. **Arithmetic Instructions**:
   - `ADD` destination, source: Adds the value in the source register to the value in the destination register and stores the result in the destination register.
   - SUB destination, source: Subtracts the value in the source register from the value in the destination register and stores the result in the destination register.

2. **Data Transfer Instructions**:
   - `LOAD` destination, memory_address: Loads the value from the specified memory address into the destination register.
   - `STORE` source, memory_address: Stores the value from the source register into the specified memory address.

3. **Branch Instructions**:
   - `JUMP` memory_address: Unconditionally jumps to the specified memory address.
   - `JZ` register, memory_address: Jumps to the specified memory address if the value in the register is zero.
   - `JNZ` register, memory_address: Jumps to the specified memory address if the value in the register is not zero.

4. **Control Instructions**:
   - HALT: Stops the execution of the program.

This is just a basic example to illustrate the major categories of instruction types. You can expand upon it by adding more instructions as per your requirements and educational goals.

To implement the simulation, you can create a file or a data structure that represents the memory of the simulated CPU. Each memory location can store an instruction or a value. Your students can create programs in this simulated machine language by writing instructions into memory locations.

To execute the program, students would read the instructions from memory sequentially, decode them, and perform the corresponding operations. They would update register values and memory contents based on the instructions executed. The simulation continues until a HALT instruction is encountered.

This approach allows students to understand the fundamentals of instruction execution, data transfer, and control flow within a simplified CPU model. It also provides them with hands-on experience in programming at a low level.

Feel free to modify or expand upon the instruction set to align with your teaching objectives and provide additional functionality.

Certainly! Here's an example of a simulated code file written in the basic machine language we discussed:

```python
; Simulated Machine Language Program

; Variable Declarations
LOAD R1, 5      ; Load the value 5 into register R1
LOAD R2, 10     ; Load the value 10 into register R2

; Arithmetic Operation
ADD R3, R1      ; Add the values in R1 and R2 and store the result in R3

; Data Transfer
STORE R3, 100   ; Store the value in R3 into memory location 100

; Control Flow
JZ R3, 200      ; Jump to memory location 200 if the value in R3 is zero
JUMP 300        ; Unconditionally jump to memory location 300

; Halt Instruction
HALT            ; Stop the execution of the program
```

In this example, we have a simple program that performs an arithmetic operation, transfers data between registers and memory, and controls the flow of execution using conditional and unconditional jumps. The program loads values into registers, performs an addition operation, and stores the result in memory. Then, based on the value in register R3, it either jumps to a specific memory location or unconditionally jumps to another location. Finally, the program halts to stop the execution.

You can store this code in a text file, read it into memory within your simulation program, and execute the instructions one by one according to the simulated machine language's semantics.

Please note that this example is very basic and intended to demonstrate the structure of the code file. You can extend and modify it as needed to cover more instructions, implement more complex programs, or introduce additional concepts based on your educational objectives.

Certainly! Here's an expanded example of simulated instructions in the basic machine language, including additional instruction types to provide a larger set of simulated instructions:

```python
; Simulated Machine Language Program

; Variable Declarations
LOAD R1, 5           ; Load the value 5 into register R1
LOAD R2, 10          ; Load the value 10 into register R2

; Arithmetic Operations
ADD R3, R1, R2       ; Add the values in R1 and R2, and store the result in R3
SUB R4, R2, R1       ; Subtract the value in R1 from the value in R2, and store the result in R4
MUL R5, R1, R2      ; Multiply the values in R1 and R2, and store the result in R5
DIV R6, R2, R1       ; Divide the value in R2 by the value in R1, and store the result in R6
MOD R7, R2, R1       ; Calculate the modulus of the value in R2 divided by the value in R1, and store the result in R7

; Data Transfer
LOAD R8, [R9]        ; Load the value from the memory address stored in R9 into register R8
STORE R10, [R9]      ; Store the value from register R10 into the memory address stored in R9

; Bitwise Operations
AND R11, R1, R2      ; Perform a bitwise AND operation between the values in R1 and R2, and store the result in R11
OR R12, R1, R2       ; Perform a bitwise OR operation between the values in R1 and R2, and store the result in R12
XOR R13, R1, R2      ; Perform a bitwise XOR operation between the values in R1 and R2, and store the result in R13
NOT R14, R1          ; Perform a bitwise NOT operation on the value in R1, and store the result in R14

; Control Flow
JZ R3, 200           ; Jump to memory location 200 if the value in R3 is zero
JNZ R4, 300          ; Jump to memory location 300 if the value in R4 is not zero
JUMP 400             ; Unconditionally jump to memory location 400
CALL 500             ; Call a subroutine at memory location 500
RET                  ; Return from a subroutine

; Input/Output
INPUT R15            ; Read input from the user and store it in R15
OUTPUT R16           ; Output the value in R16

; Halt Instruction
HALT                 ; Stop the execution of the program
```



