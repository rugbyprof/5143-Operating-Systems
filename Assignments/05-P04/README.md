## Reader Writer Part 2
#### Due: TBD


## Overview

This program will have multiple process running, all needing to execute instructions. The thing about all of these processes is that they are each readers and writers accessing the same memory. So, depending on the protection of our critical section (shared memory) the end result of each program might be different. Your goal is to write a simulation testing this theory. Your simulation should be able to spawn from 1-P programs, each with 100+ instructions, then "run" each program. Your first task is to run the programs without any memory protection. 

We also want to simulate different system conditions. This means the system may be busier some times than others. To help with this, implement a random "sleep" to be imposed on each process at random times. A busy system may impose a sleep every 7-10 instructions, and a system with a light load may impose a random sleep every 10-20 instructions. The motivation behind this is to ensure different execution paths for each process. 

If we simulate the running of all processes in this way, we should guarantee different outcomes for subsequent runs. Then we can show that using memory protection mechanisms are actually necessary sometimes. 

## Project Design

I don't care how you write your project, as long as it is readable and understandable. I have a list of class definitions below, as that is how I would approach solving the problem. You may use OOP or simply a bunch of functions. However, it should be organized in some fashion. 

## List of Classes 

### Process Control Block

We need a class the represents a `Process Control Block`. This is a structure that stores current information about a specific process. Our version will be much more abstract than actual PCB's, but the idea will be the same. 

|   #   | PCB                       |
| :---: | :------------------------ |
|   1   | Process Id                |
|   2   | Process State             |
|   3   | Priority                  |
|   4   | Register Contents         |
|   5   | Program Counter           |
|   6   | Memory Limits             |
|   7   | List of Open Files        |
|   8   | List of Devices (IO Info) |

#### Decriptions

1. Unique identifier for the process
2. Ready, Running, etc.
3. Value to identify priority (not defined right now but 1-5 would suffice where 5 is highest)
4. Contents (a copy) of the registers at time of context switch
5. Memory limits (min address => max address)
6. List any files currently opened by process
7. Io devices being used by process

So the PCB class will be responsible for maintaining a processes state through a collection of data members which get updated throughout the life of a process. In our simulation, we will probably store the instructions in the PCB as well (this is not normal) since we aren't simulating memory in a way to store instruction blocks along with the instruction results. 

### Registers

There will also be a class that represents the registers for our instructions to use. There are many different types of registers in a real system:

  - MBR: Memory Buffer Register
  - MAR: Memory Address Register
  - PC: Program Counter
  - IR: Instructions Register
  - AC: Accumulator
  - ETC ...

But we will only use registers to store values from our fake set of instructions. For this we only need two! And we will generically name them **R1 and R2**.

Our registers class will be responsible for holding two values, and the methods to manipulate those values. It only needs two data members along with methods to read or write to each location. 

See my implementation of a set of registers [here](registers.py). The class is nicely overloaded so it works like a builtin type:

```python
r = Registers(2)

r[0] = 33
r[1] = 21

print(r)
```

### Cpu

This is a class that will "execute" each instruction. As simple as each instruction is, it is important that they are executed correctly. When a process is "running" it will execute the instructions for each "process". Each process in our world lives in a file, where normally we would load instructions into memory / virtual memory and read blocks of instructions from there. We won't be doing that for this project. 

The CPU will be responsible for: 

- Breaking an instruction into its components.
- Accessing memory and loading R1 and R2 with the correct values.
- Executing the instruction and writing back the answer to the proper location.
- Updating the PCB for a process whenever a process is `context switched` off the cpu.

### Dispatcher

The dispatcher class will be responsible for scheduling processes using a round robin scheduling algorithm. The time slice or quantum will be between 7-11 clock ticks. Scheduling a process includes moving processes between running states: new, ready, running, waiting, terminated

### Instructions

For now all instructions will have the same format as the one below. Two reads from somewhere in memory, an arithmetic operation, and a write back to memory. This is an extremely simplified view of what really goes on, but fits our purposes.

```
READ A205 R1
READ B240 R2
ADD R1 R2
WRITE R1 A205
```

## Approach to Problem

- Class discussion



## Deliverables


- Place code on github with a write up describing the process of writing your project and members of your group. 
- Look [HERE](../../Resources/00-Readmees/README.md) for how to write up a readme.
- Present the outcome of your work last week of April.
- You again should visualize your output in some fashion showing the basic elements as it runs:
  - Process on CPU
  - Memory Changing and by who
- Show your program running with memory protection and with memory protection. 
- Show memory being different when race conditions are present, and show how outcomes are the same when memory is treated as a critical section.