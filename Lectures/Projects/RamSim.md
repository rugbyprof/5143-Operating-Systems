## Project X - RAM Simulation / Virtualization
#### Due: TBD


Here's an overview of a simulated RAM along with virtual memory address translation to physical addresses:

1. **Define RAM and Virtual Memory**: Create data structures to represent both RAM and virtual memory. RAM represents the physical memory available in the system, while virtual memory represents the address space used by a program.

2. **RAM Organization**: Define the organization of RAM, which consists of memory cells or bytes. Each memory cell can store a fixed-size value (e.g., 8 bits or 16 bits). Allocate appropriate memory capacity for the simulated RAM.

3. **Virtual Memory Address Translation**: Implement the address translation mechanism to convert virtual addresses used by the program to physical addresses in RAM. The translation process typically involves splitting the virtual address into page number and page offset. Use the page table from the virtual memory simulation to map the virtual page number to the corresponding physical frame number.

4. **Page Fault Handling**: When a translation results in a page fault (i.e., the requested page is not present in RAM), you can simulate the page fault handling process. Apply the page replacement algorithm from the virtual memory simulation to select a victim page from RAM and replace it with the requested page from virtual memory. Update the page table accordingly.

5. **Memory Access Simulation**: As you simulate the execution of instructions in the machine language program, track memory accesses. When an instruction references a virtual address, use the address translation mechanism to translate it to a physical address in RAM. Handle page faults if necessary.

6. **Monitoring and Metrics**: Collect statistics during the simulation, such as page fault rates, hit rates, and the behavior of the page replacement algorithm. These metrics provide insights into the performance and behavior of the simulated RAM and virtual memory system.

By simulating RAM and virtual memory together, you can demonstrate the interaction between the two and showcase the address translation process. This allows students to understand how virtual memory helps manage larger address spaces than physically available RAM.
