## Project X - ALU Simulation / Virtualization
#### Due: TBD


Here's a breakdown of the `ALU` (Arithmetic Logic Unit) component for your simulation, including its functions and usage:

**ALU (Arithmetic Logic Unit):**
The ALU is responsible for performing `arithmetic` and `logical` operations on data. It operates on data stored in registers and updates the result accordingly.

1. **Arithmetic Operations:**
   - The `ALU` performs various arithmetic operations, such as `addition`, `subtraction`, `multiplication`, and `division`.
   - It operates on numeric data, typically stored in registers, and computes the result.

2. **Logical Operations:**
   - The `ALU` performs logical operations, such as `AND`, `OR`, `NOT`, and `XOR`.
   - It operates on `binary data`, typically stored in `registers`, and performs `bitwise operations`.

3. **Comparison Operations:**
   - The `ALU` compares two values and sets `condition flags` or `registers` based on the result.
   - Comparison operations include checks for `equality`, `greater than`, `less than`, and other r`elational conditions`.

4. **Shift and Rotate Operations:**
   - The `ALU` performs `shift` and `rotate` operations on binary data, shifting the bits left or right or rotating them.
   - These operations are used to manipulate data or perform `bitwise calculations`.

5. **Overflow and Carry Detection:**
   - The `ALU` detects `overflow` or `carry conditions` that occur during arithmetic operations.
   - Overflow occurs when the result of an arithmetic operation exceeds the maximum range that can be represented.
   - Carry occurs when there is a need to carry a bit from one operation to the next, such as in addition or shifting.

6. **Flag or Status Register Updates:**
   - The `ALU` updates flag or status registers to reflect the outcome of operations.
   - Common flags include `zero flag` (indicating a zero result), `carry flag` (indicating a carry or borrow), and `overflow flag` (indicating overflow).

7. **Control Flow Operations:**
   - The `ALU` supports control flow operations, such as `jumps`, `conditional branches`, and `subroutine calls`.
   - These operations modify the `program counter` (PC) to redirect the program's execution flow.

8. **Data Movement Operations:**
   - The `ALU` can facilitate data movement between registers or memory locations.
   - This includes operations like `loading data` from memory into a register or `storing data` from a register to memory.

