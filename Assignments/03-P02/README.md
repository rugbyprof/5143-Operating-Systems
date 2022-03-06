## Cpu Scheduling - Simulation
#### Due: 03-07-2022 (Monday @ 2:30 p.m.)


### Job State
<center>
<img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/process-diagram.gif" width="400">
</center>

- NEW - The process is being created, and has not yet begun executing.
- READY - The process is ready to execute, and is waiting to be scheduled on a CPU in the "ready queue".
- RUNNING - The process is currently executing on a CPU.
- WAITING (BLOCKED) - The process has temporarily stopped executing, and is waiting on an I/O request to complete.
- TERMINATED - The process has completed.

### First-Come First-Serve Scheduling, FCFS

- FCFS is very simple - Just a FIFO queue, like customers waiting in line at the bank or the post office or at a copying machine.
- FCFS suffers from the convoy effect ... a long job shows up first and blocks everyone else from getting the CPU.

### Shortest-Job-First Scheduling, SJF

<center>
<img src="https://cs.msutexas.edu/~griffin/zcloud/zcloud-files/SJF.jpg" width="400">
</center>

- The idea behind the SJF algorithm is to pick the quickest fastest little job that needs to be done, get it out of the way first, and then pick the next smallest fastest job to do next.
( Technically this algorithm picks a process based on the next shortest CPU burst, not the overall process time. )

- SJF can be proven to be the fastest scheduling algorithm, but it suffers from one important problem: How do you know how long the next CPU burst is going to be?

- Usually the system would use some algorithm or statistics to "guess" the next shortest burst based on historical information. We are going to know based on the input data.


### Priority Scheduling

- Priority scheduling is a more general case of SJF, in which each job is assigned a priority and the job with the highest priority gets scheduled first. ( SJF uses the inverse of the next expected burst time as its priority - The smaller the expected burst, the higher the priority. )

  - Priority scheduling can be either **preemptive** or **non-preemptive**.
  - Priority scheduling can suffer from a major problem known as indefinite blocking, or starvation, in which a low-priority task can wait forever because there are always some other jobs around that have higher priority.

  - One common solution to this problem is aging, in which priorities of jobs increase the longer they wait. 

### Round Robin Scheduling

- Round robin scheduling is similar to FCFS scheduling, except that CPU bursts are assigned with limits called time quantum.
- When a process is given the CPU, a timer is set for whatever value has been set for a time quantum.
- If the process finishes its burst before the time quantum timer expires, then it is swapped out of the CPU just like the normal FCFS algorithm.
- If the timer goes off first, then the process is swapped out of the CPU and moved to the back end of the ready queue.

### Multiple-Processor Scheduling
- When multiple processors are available, then the scheduling gets more complicated, because now there is more than one CPU which must be kept busy and in effective use at all times.
- Load sharing revolves around balancing the load between multiple processors.
- Multi-processor systems may be **heterogeneous**, ( different kinds of CPUs ), or **homogenous**, ( all the same kind of CPU ). Even in the latter case there may be special scheduling constraints, such as devices which are connected via a private bus to only one of the CPUs. This book will restrict its discussion to homogenous systems.
- Approaches to Multiple-Processor Scheduling
  - One approach to multi-processor scheduling is **asymmetric multiprocessing**, in which one processor is the master, controlling all activities and running all kernel code, while the other runs only user code. This approach is relatively simple, as there is no need to share critical system data.
  - Another approach is **symmetric multiprocessing**, **SMP**, where each processor schedules its own jobs, either from a common ready queue or from separate ready queues for each processor.

## Requirements

- This program is not a true system program, it is just a typical user application that requires no spawning of processes, no timer interrupt handling, no I/O interrupt handling, etc. It is a **simulation**
- Your program must use some form of "visual presentation" to show, at least, the following four components:
  - A CPU
  - A ready queue showing all the processes waiting to be dispatched to use the CPU
  - An I/O device
  - An I/O queue showing all the processes waiting to use the I/O device
- Your choice of "visual presentation" can be either a text-mode "ASCII art" using something NCurses or a GUI program with something like [DearPyGui](https://github.com/hoffstadt/DearPyGui)
  
- The description of a simulated process includes the following information:
  - Arrival time (t<sub>a</sub>) of the process
  - Process ID (pid)
  - A series of CPU bursts interleaved with IO bursts. 
    - CPU burst durations (cpu<sub>i</sub>, i = 1, 2, ..., n), 
    - I/O burst durations (io<sub>j</sub>, j = 1, 2, ..., n-1)
 - This will all be written in one line of the input file (the name of the input file will be passed as the first command-line argument to your program) in the following order:
    - t<sub>a</sub>pid cpu<sub>1</sub> io<sub>1</sub> cpu<sub>2</sub> io<sub>2</sub> ... cpu<sub>n-1</sub> io<sub>n-1</sub> cpu<sub>n</sub>
- A process always begins and ends with a CPU burst. 
- All the numbers are integers.
- A Time quantum (integer) used in the Round Robin simulation is given as the second command-line parameter.
- The simulator shall print an appropriate message when a simulated process changes its state. 
- We are using the 5-state model (New, Ready, Running, Waiting, Terminated). 
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
