## Reader Writer Part 2 - Simulating Race Conditions
#### Due: 04-25-2022 (Wednesday @ 2:30 p.m.)


## Overview

This program will have multiple processes (programs) running, all needing to execute instructions. Each program will read from and write to memory. A certain portion of memory is considered "shared" and processes must gain locks when updating that portion of memory. Depending on the protection of our critical section (shared memory) the end result of each program might be different. Your goal is to write a simulation testing this theory. Your simulation should be able to spawn from 1-P programs, each with 100+ instructions, then "run" each program ~~as its own thread~~. 

As each program runs, they will read from and write to memory in an order determined by our own schedular. ~~Of course, the system schedular will perform its own context switches at the OS level, but that shouldn't effect the results of each run~~. The use of locks in programs that access shared memory is important in order to have confidence in the final values calculated at the end of the run.

In order to simulate different system conditions there will be a random "sleep" imposed on each process at random times. A busy system may impose a sleep every 7-10 instructions, and a system with a light load may impose a random sleep every 10-20 instructions. The motivation behind this is to ensure different execution paths for each process. 

If we simulate the running of all processes in this way, we should guarantee different outcomes for subsequent runs. Then we can show that using memory protection mechanisms are actually necessary sometimes. 

## Instructions

Instructions are randomly generated and are similar to the one below. In addition to the READ, WRITE operations and the ADD, SUB, MUL, DIV  there is an additional LOAD operations for privileged instructions which will load the process id into register 3 (R3) and an integer value into R4. This value is the privileged id counter (`PIC`). This also means you cannot execute a privileged instruction until R4 contains `PIC - 1`. 

```
   [
      "READ B100 R2",
      "READ C125 R1",
      "MUL R2 R1",
      "WRITE R2 B100",
      "READ P165 R1",
      "READ B125 R2",
      "MUL R1 R2",
      "WRITE R1 P165",
      "LOAD 4 R3",
      "LOAD 26 R4"
   ]
```

In order to access the privileged memory section, you need to acquire a lock. Not a threading lock, but a lock of our own design:

```python
class Lock(Borg):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.locked = False
        self.waitQ = []

    def __str__(self):
        s = str(id(self)) + "\n"
        for k, v in self.__dict__.items():
            s += f"{k}={v}\n"
        return s

    def acquire(self):
        if not self.locked:
            if id(self) in self.waitQ:
                self.waitQ.remove(id(self))
            self.locked = True
            return True
        return False

    def release(self):
        if self.locked:
            self.locked = False
            return True
        return False

    def wait(self):
        self.waitQ.append(id(self))
```

This lock allows processes to `acquire`, `release`, OR `wait` for the lock to come available via a built in queue. 

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

## Requirements

- Write an object oriented solution that will simulate the running of multiple processes by executing instructions on a simulated CPU. 
- You will have a dispatcher scheduling processes using a Round Robin algorithm. 
- Run your simulation without regard to ordering privileged instructions to view a memory snapshot at completion. 
- Change all the sleep values for each process, and look at the memory snapshot again.
- Now order the privileged instructions using our software lock and view memory results.
- Finally, again change all the sleep values, and ensure that privileged memory output does not change when the instructions are ordered properly

**- Visualize your output for your presentation**
  - Maybe show cpu and register contents 
  - Show progress of programs running (percent complete)
  - Show (possibly) shared memory as it changes

## Deliverables


- Place code on github with a write up describing the process of writing your project and members of your group. 
- Look [HERE](../../Resources/00-Readmees/README.md) for how to write up a readme.
- Present the outcome of your work last week of April.




https://realpython.com/intro-to-python-threading/

https://medium.com/geekculture/distributed-lock-implementation-with-redis-and-python-22ae932e10ee

https://www.laurentluce.com/posts/python-threads-synchronization-locks-rlocks-semaphores-conditions-events-and-queues/
