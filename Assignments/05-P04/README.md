## Reader Writer Part 2

#### Due: TBD

## Process Control Block

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

### Decriptions

1. Unique identifier for the process
2. Ready, Running, etc.
3. Value to identify priority (not defined right now)
4. Contents (copy) of the registers at time of context switch
5. Memory limits (min address => max address)
6. List any files currently opened by process
7. Io devices being used by process

So the PCB class will be responsible for maintaining a processes state through a collection of data members which get updated throughout the life of a process. In our simulation, we will probably store the instructions in the PCB as well (this is not normal) since we aren't simulating memory in a way to store instruction blocks along with the instruction results. 

## Registers

There will also be a class that represents the registers for our instructions to use. There are many different types of registers in a real system:

  - MBR: Memory Buffer Register
  - MAR: Memory Address Register
  - PC: Program Counter
  - IR: Instructions Register
  - ETC ...

But we will only use registers to store values from our fake set of instructions. For this we only need two! 

Our registers class will be responsible for holding two values, and the methods to manipulate those values. It only needs two data members along with methods to read or write to each location. 

## Cpu

This is a class that will "exectute" each instruction. As simple as each instruction is, it is important that they are executed correctly. When a process is "running" it will execute the instructions for each "process". Each process in our world lives in a file, where normally we would load instructions into memory / virtual memory and read blocks of instructions from there. We won't be doing that for this project. 

The CPU will be responsible for: 

- Breaking an instruction into its components.
- Accessing memory and loading R1 and R2 with the correct values.
- Executing the instruction and writing back the anwswer to the proper location.
- Updating the PCB for a process whenever a process is `context switched` off the cpu.

## Dispatcher

The dispatcher class will be responsoble for scheduling processes using a round robin scheduling algorithm. The time slice or quantum will be between 7-11 clock ticks. Scheduling a process includes moving processes between running states: new, ready, running, waiting, terminated

## Instructions

For now all instructions will have the same format as the one below. Two reads from somewhere in memory, an arithmetic operation, and a write back to memory. This is an extremely simplified view of what really goes on, but fits our purposes.

```
READ A205 R1
READ B240 R2
ADD R1 R2
WRITE R1 A205
```

