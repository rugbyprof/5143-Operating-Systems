## Cpu Scheduling - Simulation

#### Due: 11-12-2024 (Week of Nov 12<sup>th</sup>)

Cpu scheduling is a classic and contemporary computer science problem that started when early computers had processors that remained idle much of the time. The goal initially was to get multiple programs loaded into memory, so they could run back to back. This was still inefficient and needed improvement. That soon evolved into multiple programs loaded into memory and when one process blocked itself, the cpu would work on another available process (multi-programming). This, of course, kept evolving into our multi-threaded / multi-processor world. Yet, we still need to be cognizant of keeping the cpu(s) busy! So what does a scheduler do?

### Scheduler

A scheduler makes choices in order to minimize or maximize a set of criteria, where the criteria really can be simplified into this one concept: "minimize the time any process is doing nothing". However we measure that, or label it, its the crux of the scheduling problem.

#### Goals

1. _`Maximizing Throughput`_ (the total amount of work completed per time unit)
2. _`Minimizing Wait Time`_ (time from work becoming ready until the first point it begins execution) (We define it slightly differently)
3. _`Minimizing Latency`_ or response time (time from work becoming ready until it is finished)
4. _`Maximizing Fairness`_ (equal CPU time to each process, or more generally appropriate times according to the priority and workload of each process).

- In practice, these goals often conflict (e.g. throughput versus latency), thus a scheduler will implement a suitable compromise.
- Preference is measured by any one of the concerns mentioned above, depending upon the user's needs and objectives.

The scheduler will attempt to accomplish the above goals by moving a process around through a series of states. Of course each process has its own unique set of needs (IO intensive, CPU intensive for example), and the scheduler cannot change what the process needs or when it needs it. Its power is in determining when a process gets access to a resource, the most important of which is the CPU. If it's smart about the order in which it allows access, then the above goals can be met.

As I mentioned, the scheduler moves processes around through a series of states, based on the processes needs. Our simulation will be implementing the most basic set of states, in which there are five (see below).

### Job State

<center>
<img src="https://images2.imgbox.com/0e/ee/Ip7dYsgz_o.png" width="500">
</center>

1. **NEW** - The process is being created, and has not yet begun executing.
2. **READY** - The process is ready to execute, and is waiting to be scheduled on a CPU.
3. **RUNNING** - The process is currently executing on a CPU.
4. **WAITING** (BLOCKED) - The process has temporarily stopped executing, and is waiting on an I/O request (peripheral device to come open).
5. **IO** - Process has gained access to one of the peripheral devices.
6. **TERMINATED** - The process has completed.

Each state is represented as a queue that holds each process that is currently in that state. The success or failure of scheduling boils down to moving each process from queue to queue in an efficient and consistent manner. Efficiency depends on multiple factors, the main one being the actual scheduling algorithm choosing which process gets cpu time or resource time. The next section discusses the algorithms your simulation needs to implement.

## Scheduling Algorithms

#### First-Come-First-Serve, FCFS

- FCFS is very simple - FIFO simply queues processes in the order that they arrive in the ready queue.
- This is the simplest scheduling algorithm.
- This is a **non-preemptive** scheduling algorithm.
- Context switches only occur upon cpu burst termination.
- **Example**:
  - _P<sub>n</sub>_ is first to arrive and has a 35 time unit cpu burst.
  - Once it is in the `Running` state it will stay there until its burst is complete and it moves to the `Wait` queue.
  - After it finishes its `IO` burst, it comes back to the `Ready` queue at the end of the line and waits for the next open cpu.

#### Round-Robin, RR

- The scheduler assigns a fixed time unit per process known as a time-slice or time-quantum, and cycles through each process equally.
- If the process completes within that time-slice it gets terminated otherwise it is rescheduled after giving a chance to all other processes.
- This is a **preemptive scheduling** algorithm.
- **Example**:
  - _P<sub>n</sub>_ is first to arrive and has a 35 time unit cpu burst.
  - Once it is in the `Running` state it will stay there until its `time-slice` is up, in which it will be interrupted and sent to the end of the `Ready` queue.
  - It will continue this circular cycle until it finishes its cpu burst. So if the `time-slice` is 5, then it will have five rounds of `Running`->`Ready` before it can finally go to the `Wait` queue and start its `IO` burst.
  - The `Wait` queue has no `time-slice` so once it gains an `IO` device it keeps it until the burst is over and then back to the `Ready` queue``

#### Priority-Based, PB

- The operating system assigns a fixed priority rank to every process, and the scheduler arranges the processes in the ready queue in order of their priority.
- Lower-priority processes get interrupted by incoming higher-priority processes.
- This is a **preemptive scheduling** algorithm.
- Runs into possibility of starving processes with low priorities.
- I think we can postulate what would happen if we do not implement some kind of `promotion` for low priority processes.
- I will leave it up to you how you handle it. It does not have to be something complicated, it could be based on total time in system (which is tracked per process anyway) or even some random promotion event. Use your imagination.
- **Example1**:
  - _P<sub>n</sub>_ is first to arrive and has a 35 time unit cpu burst and the highest priority.
  - Next however many processes to arrive get a big so what and have to wait.
- **Example2**:
  - _P<sub>n</sub>_ is first to arrive and has a 35 time unit cpu burst and the lowest priority.
  - _P<sub>n+1</sub>_ is next to arrive and has a 10 time unit cpu burst and a medium priority, it interrupts _P<sub>n</sub>_ sending to the place in the ready queue equivalent to its priority and takes over the cpu.
  - _P<sub>n+2</sub>_ is next to arrive and has a 100 time unit cpu burst and the highest priority, it interrupts _P<sub>n+1</sub>_ sending it to the place in the ready queue equivalent to its priority and takes over the cpu. And stays since it cannot be preempted via priority.

#### Shortest-Job-First, SJF (Do Not Implement)

- Shortest job first (SJF) also known as Shortest job next (SJN) or shortest process next (SPN), is a scheduling policy that selects for execution the waiting process with the smallest execution time.
- SJF is a **non-preemptive** algorithm
- A disadvantage of using shortest job next is that the total execution time of a job must be known before execution. But we know, so we can implement it.
- Total Execution Time = Sum(cpuBurst<sub>**1**</sub>+cpuBurst<sub>**2**</sub>+cpuBurst<sub>**3**</sub>+...+cpuBurst<sub>**n**</sub>)

#### Shortest-Remaining-Time, SRT (Do Not Implement)

- Shortest remaining time, also known as shortest remaining time first (SRTF), is a scheduling method that is a **preemptive version** of shortest job next scheduling.
- In this scheduling algorithm, the process with the smallest amount of time remaining until completion is selected to execute.
- Since the currently executing process is the one with the shortest amount of time remaining by definition, and since that time should only reduce as execution progresses, the process will either run until it completes or get preempted if a new process is added that requires a smaller amount of time.
- Execution Time Remaining = Sum of remaining cpuBursts.

### MLFQ (Multi Level Feedback Queue)

- Coming soon

#### CFS (Completely Fair Scheduler)

- Coming soon

## Resources

The goal of each process is to gain access to a resource at the time it needs it, so that it can complete its lifecycle. In class we discussed implementing queues for each state. All of them unbounded with the exception of a single cpu. Well, now I would like a little more control over the amount of available resources. In the table below, you can see all the queues are `unbounded` but now we are adding a bounded size on the `IO` queue.

<center>
<img src="https://images2.imgbox.com/51/6c/ju18lbUX_o.png" width="250">
</center>

To emphasize the resource issue again, I need to mention that the number of resources heavily influences throughput. Resources go up, throughput gets better. We are making each IO device generic for ease of implementation, but if many process were waiting for a specific device, no matter how many total IO devices there are, then through put could suffer. For ease of implementing this simulation, all resources will be categorized as one of two things: a `CPU`, or an `IO` device.

### Processors

In fact, all CPU's (processors) are assumed to be the same. This means we do not need to worry about **heterogeneous** or **homogenous** processors.

> - **heterogeneous**: different processor types. Usually meaning one would run kernel code and others everything else, or one cpu being the "cpu in charge" delegating to others.
> - **homogenous**: all cpu's the same type. But could still mimic above strategy regardless.

In our simulation a cpu is available to any and all processes, and we will have the ability to change the number of cpu's based on the current simulation run. I will say that `1-4 cpu's` is what we will go with.

### IO Devices

Likewise, we will not distinguish between different types of IO devices (like printers, network cards, disks, etc.). So, again, when you write code to implement an IO device, you can simply create duplicate instances to increase the number of devices for processes to use during their IO bursts. `In this case I think 3 - ?? devices?` We should discuss more in class to determine a good number to run our sims.

## Input Files

Use the program `generate_input.py` to make different types of input files. The default values in the program are helpful, but you should run the script with a minimum of three file types:

- Cpu Intensive Process (Lots of cpu time vs little IO time)
- IO Intensive Process (Lots of IO time vs little cpu time)
- Prioritized with lots of high priority (few low priorities)

- A process always begins and ends with a CPU burst.
- All the numbers are integers.

- The description of a simulated process includes the following information:
  - Arrival time (AT<sub>t</sub>) of the process
  - Process ID (PID<sub>i</sub>)
  - Priority (P<sub>p</sub>)
  - CPU burst durations (cpub<sub>i</sub>, i = 1, 2, ..., N),
  - I/O burst durations (iob<sub>j</sub>, j = 1, 2, ..., N-1)
- This will all be written in one line of the input file (the name of the input file will be passed as the first command-line argument to your program) in the following order:

> AT<sub>t</sub> PID<sub>i</sub> P<sub>p</sub> cpub<sub>1</sub> iob<sub>1</sub> cpub<sub>2</sub> iob<sub>2</sub> ... cpub<sub>n</sub>

### No Pressure

- Remember this is a simulation, where the system clock (aka timer) is simply an integer variable incremented in some loop construct.
- We will read the the processes that will run in our simulation from multiple files, where each file will emphasize a different type of load (see previous).
- This program is not a true system program, it is just a typical user application that requires no spawning of processes, no timer interrupt handling, no I/O interrupt handling, etc. It is a **simulation**

#### Basic High Level Algorith

1. Jobs arrive at time `N`, and enter the `New` queue.
2. Any jobs already in the `New` queue go to the `Ready` queue.
3. Decrement burst times on Cpu(s), if any are zero, move to `Wait` queue.
4. Decrement burst times on Peripheral(s), if any are zero, move to `Ready` queue.
5. If any Cpu(s) are free, take next from `Ready` queue.
6. If any Periphal(s) are free, take next from `Wait` queue.
7. Do accounting for each process in the appropriate queues when appropriate (basically if it hasn't just been moved).

## Requirements

#### Visualization

- Your program must use some form of "visual presentation" to show:
  - Each of the 6 queues [New, Ready, Running, Waiting, IO, Exit] and which processes are in them
- Your choice of "visual presentation" can be NCurses or a GUI program with something like [DearPyGui](https://github.com/hoffstadt/DearPyGui) or my [Rich Example](../../Resources/06-Rich_Example/)
- Specific messages at some time throughout the simulation. Obviously for presentation purposes we will do short runs with small files. If you were to use my Python Rich table example, you could print messages below the table in a panel or similar.

#### Presentation

- You should have 6 runs ready to present, 2 of each scheduling type.
- Depending on the scheduling algorithm, you should be able to choose the specs from the command line.

  - Example:
    - `python sim.py sched=RR timeslice=3 cpus=4 ios=6 input=filename.dat`
    - `python sim.py sched=FCFS cpus=2 ios=2 input=otherfile.dat`
    - `python sim.py sched=PB cpus=2 ios=2 input=highpriorityfile.dat`

- The messages that should print as your presentation runs are listed below.
- Coloring times, process's, cpu's, and device's would be preferred.
- Messages:

  - At t<sub>n</sub> job _p<sub>n</sub>_ entered new queue.
    - Ex: At t:31 job p12 entered new queue
  - At t<sub>n</sub> job _p<sub>n</sub>_ obtained _cpu<sub>n</sub>_
    - Ex: At t:35 job p12 obtained cpu:0
  - At t<sub>n</sub> job _p<sub>n</sub>_ obtained _device<sub>n</sub>_
    - Ex: At t:44 job p15 obtained device:2

- When a process terminates, the output should give that jobs stats. The stat acronyms are as follows:
  - ST = Time entered system
  - TAT = Turn Around Time (time exited system - time entered)
  - RWT = Time spent in ready queue
  - IWT = Time spent in wait queue
- Example:

  - Job _p<sub>n</sub>_ TAT = _t<sub>n</sub>_, RWT = _t<sub>n</sub>_, IWT = _t<sub>n</sub>_
  - Job p:23 ST = 101 TAT = 545, RWT = 121, IWT = 211

- At the end of simulation, the simulator should display the percentage of CPU utilization, average TAT, average ready wait time, and average I/O wait time.

### Complete Runs And Output

- You need aggregate data for jobs consisting of:

  - Scheduling Algorithms: [FCFS, RR, PB]
  - Cpus: [1,2,3,4]
  - Devices: [2,4,6]
    > Note: For Round Robin you need to change the time quantum: [3,5,7,9]

- We can discuss how to output this in a csv in class.

## Deliverables

- Place code on github with a write up describing the process of writing your project and members of your group.
- Look [HERE](../../Resources/00-Readmees/README.md) for how to write up a readme.
- Present your results in class when specified
- Ensure your presentation follows guidelines above``
