## Cpu Scheduling - Simulation
#### Due: 11-06-2023 (Week of the 6<sup>th</sup>)


Cpu scheduling is a classic and contemporary computer science problem that started when early computers had processors that remained idle much of the time. The goal initially was to get multiple programs loaded into memory, so they could run back to back. This was still inefficient and needed improvement.  That soon evolved into multiple programs loaded into memory and when one process blocked itself, the cpu would work on another available process (multi-programming). This, of course, kept evolving into our multi-threaded / multi-processor world. Yet, we still need to be cognizant of keeping the cpu(s) busy! So what does a scheduler do?

### Scheduler

A scheduler makes choices in order to minimize or maximize a set of criteria, where the criteria really can be simplified into this one concept: "minimize the time any process is doing nothing". However we measure that, or label it, its the crux of the scheduling problem.

#### Goals

1. Maximizing throughput (the total amount of work completed per time unit)
2. Minimizing wait time (time from work becoming ready until the first point it begins execution) (We define it slightly differently)
3. Minimizing latency or response time (time from work becoming ready until it is finished)
4. maximizing fairness (equal CPU time to each process, or more generally appropriate times according to the priority and workload of each process).
   
- In practice, these goals often conflict (e.g. throughput versus latency), thus a scheduler will implement a suitable compromise. 
- Preference is measured by any one of the concerns mentioned above, depending upon the user's needs and objectives.

The scheduler will attempt to accomplish the above goals by moving a process around through a series of states. Of course each process has its own unique set of needs (IO intensive, CPU intensive for example), and the scheduler cannot change what the process needs or when it needs it. Its power is in determining when a process gets access to a resource, the most important of which is the CPU. If it's smart about the order in which it allows access, then the above goals can be met. 

As I mentioned, the scheduler moves processes around through a series of states, based on the processes needs. Our simulation will be implementing the most basic set of states, in which there are five (see below). 

### Job State
<center>
<img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/job_state_diagram.png" width="700">
</center>

1. NEW - The process is being created, and has not yet begun executing.
2. READY - The process is ready to execute, and is waiting to be scheduled on a CPU in the "ready queue".
3. RUNNING - The process is currently executing on a CPU.
4. WAITING (BLOCKED) - The process has temporarily stopped executing, and is waiting on an I/O request to complete.
5. TERMINATED - The process has completed.

Each state is represented as a queue that holds each process that is currently in that state. The success or failure of scheduling boils down to moving each process from queue to queue in an efficient and consistent manner. Efficiency depends on multiple factors, the main one being the actual scheduling algorithm choosing which process gets cpu time or resource time. The next section discusses the algorithms your simulation needs to implement.  

## Scheduling Algorithms

#### First-Come-First-Serve, FCFS

- FCFS is very simple - FIFO simply queues processes in the order that they arrive in the ready queue.
- This is the simplest scheduling algorithm. 
- This is a **non-preemptive** scheduling algorithm.
- Context switches only occur upon cpu burst termination.

#### Shortest-Job-First, SJF

- Shortest job first (SJF) also known as Shortest job next (SJN) or shortest process next (SPN), is a scheduling policy that selects for execution the waiting process with the smallest execution time.
- SJF is a **non-preemptive** algorithm
- A disadvantage of using shortest job next is that the total execution time of a job must be known before execution. But we know, so we can implement it.
- Total Execution Time = Sum(cpuBurst<sub>**1**</sub>+cpuBurst<sub>**2**</sub>+cpuBurst<sub>**3**</sub>+...+cpuBurst<sub>**n**</sub>)

#### Shortest-Remaining-Time, SRT

- Shortest remaining time, also known as shortest remaining time first (SRTF), is a scheduling method that is a **preemptive version** of shortest job next scheduling. 
- In this scheduling algorithm, the process with the smallest amount of time remaining until completion is selected to execute. 
- Since the currently executing process is the one with the shortest amount of time remaining by definition, and since that time should only reduce as execution progresses, the process will either run until it completes or get preempted if a new process is added that requires a smaller amount of time.
- Execution Time Remaining = Sum of remaining cpuBursts. 

#### Priority-Based, PB

- The operating system assigns a fixed priority rank to every process, and the scheduler arranges the processes in the ready queue in order of their priority. 
- Lower-priority processes get interrupted by incoming higher-priority processes.
- This is a **preemptive scheduling** algorithm.
- Runs into possibility of starving processes with low priorities.

#### Round-Robin, RR

- The scheduler assigns a fixed time unit per process known as a time-slice or time-quantum, and cycles through each process equally. 
- If the process completes within that time-slice it gets terminated otherwise it is rescheduled after giving a chance to all other processes.
- This is a **preemptive scheduling** algorithm.

## Resources

Our simulation is implementing the simplest process state diagram, one that has five states. Two of those states represent processes that are waiting for resources (ready queue, and wait queue). One of those states represents a process that is running (gained access to cpu). It does not have a state in which a process has been assigned an IO device. So, lets add the "state" just to make sure we will treat IO similar to cpu. We know the cpu gets processes from the ready queue and that we can have multiple cpu's, allowing more than one process to run concurrently. The same goes for IO devices. The wait queue will give IO devices to a process as they become available. 

<center>
<img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/job_state_diagram_with_IO.png" width="700">
</center>

 To emphasize the resource issue again, I need to mention that the number of resources heavily influences throughput. Resources go up, throughput gets better. We are making each IO device generic for ease of implementation, but if many process were waiting for a specific device, no matter how many total IO devices there are, then through put could suffer. For ease of implementing this simulation, all resources will be categorized as one of two things: a CPU, or an IO device.

### Processors
In fact, all CPU's (processors) are assumed to be the same. This means we do not need to worry about **heterogeneous** or **homogenous** processors. 

>- **heterogeneous**: different processor types. Usually meaning one would run kernel code and others everything else, or one cpu being the "cpu in charge" delegating to others.
>- **homogenous**: all cpu's the same type. But could still mimic above strategy regardless. 

In our simulation a cpu is available to any and all processes.

### IO Devices

Likewise, we will not distinguish between different types of IO devices (like printers, network cards, disks, etc.). So, again, when you write code to implement an IO device, you can simply create duplicate instances to increase the number of devices for processes to use during their IO bursts. 

## Input Files

Use the program `generate_input.py` to make different types of input files. The default values in the program are helpful, but you should run the script with a minimum of three file types:

- Cpu Intensive Process (Lots of cpu time vs little IO time)
- IO Intensive Process (Lots of IO time vs little cpu time)
- Prioritized with lots of high priority  (few low priorities)

- A process always begins and ends with a CPU burst. 
- All the numbers are integers.

- The description of a simulated process includes the following information:
  - Arrival time (AT<sub>t</sub>) of the process
  - Process ID (PID<sub>i</sub>)
  - Priority (P<sub>p</sub>)
  - CPU burst durations (cpub<sub>i</sub>, i = 1, 2, ..., N), 
  - I/O burst durations (iob<sub>j</sub>, j = 1, 2, ..., N-1)
- This will all be written in one line of the input file (the name of the input file will be passed as the first command-line argument to your program) in the following order:

>AT<sub>t</sub> PID<sub>i</sub> P<sub>p</sub> cpub<sub>1</sub> iob<sub>1</sub> cpub<sub>2</sub> iob<sub>2</sub> ... cpub<sub>n</sub> 

### Comments

- Remember this is a simulation, where the system clock (aka timer) is simply an integer variable incremented in some loop construct.
- We will read the the processes that will run in our simulation from multiple files, where each file will emphasize a different type of load (see previous).
- This program is not a true system program, it is just a typical user application that requires no spawning of processes, no timer interrupt handling, no I/O interrupt handling, etc. It is a **simulation**


### Requirements

- Your program must use some form of "visual presentation" to show, at least, the following four components:
  - A CPU
  - A ready queue showing all the processes waiting to be dispatched to use the CPU
  - An I/O device
  - An I/O queue showing all the processes waiting to use the I/O device
- Your choice of "visual presentation" can be either a text-mode "ASCII art" using something NCurses or a GUI program with something like [DearPyGui](https://github.com/hoffstadt/DearPyGui)
  

- A Time quantum (integer) used in the Round Robin simulation is given as the second command-line parameter.
- The simulator shall print an appropriate message when a simulated process changes its state. 
- For instance, it shall print a message when it performs one of the following actions:
  - Starts a new process
  - Schedules a process to run
  - Moves a process to the I/O Waiting (Blocked) State
  - Preempts a process from the Running State
  - Moves a process back into the Ready State (due to I/O completion)
  - Starts servicing a process' I/O request
- Each message shall be prefixed with the current simulation time.
- When a simulated process is interrupted (because its current CPU burst is longer than the quantum) the process is preempted and re-enters the ready queue
- When a simulated process completes its current CPU burst, it will then use its I/O burst, the simulator change the process' state to Blocked. At this point, the CPU becomes idle and the dispatcher may select another process from the ready queues.
- The simulated system can have more than one CPU and more than one I/O device (we will discuss this in class). The I/O request of a process will be performed only if the I/O device is available. Otherwise, the process requesting the I/O operation will have to wait until the device is available. I/O is handled by the simulated device on first-come-first-serve basis.
- Upon completion of its I/O burst, a process will change from Blocked state to Ready and join the Ready Queue again.
- A process entering the ready queue can be one of the following:
  - a new process,
  - a process returning from Blocked state, or
  - a process preempted from the CPU
- When these three events happen at the same time, the new process will enter the Ready Q first, followed by process returning from Blocked state, and finally by the preempted process.
- When a simulated process terminates, the simulator then outputs a statement of the form:
  - Job %d terminated: TAT = %d, Wait time = %d, I/O wait = %d
- where 
  - "TAT" is Turn Around Time, 
  - "Wait time" is the total time spent by a process in the Ready Queue, 
  - "I/O wait" is the total amount of time the process had to wait for the I/O device.
- At the end of simulation, the simulator shall display the percentage of CPU utilization, average TAT, average wait time, and average I/O wait time.

### Parameterized Runs
- Each run will require 3 inputs:
   - Scheduling algorithm
   - Num Cpus
   - Num IO Devices 
- Or one config file:
   - {}

- Sources:
  - https://en.wikipedia.org/wiki/Scheduling_(computing)

## Deliverables

- Place code on github with a write up describing the process of writing your project and members of your group. 
- Look [HERE](../../Resources/00-Readmees/README.md) for how to write up a readme.
- Present your results in class last week of April.
- Look at requirements for how to visualize your code.