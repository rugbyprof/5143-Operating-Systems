# Project X - CPU Scheduling Simulation

#### Due: TBD

## 🧠 Why CPU Scheduling?

When multiple processes are ready to run, but only one CPU is available, the OS must **choose** which process gets the CPU next. This decision impacts:

- **CPU utilization**
- **System responsiveness**
- **Fairness**
- **Throughput**

---

## 🧮 Types of Scheduling Algorithms

Here's a high-level breakdown of **common CPU scheduling algorithms**:

| Algorithm                                | Preemptive? | Key Feature                  | Good For                       | Drawbacks                                        |
| ---------------------------------------- | ----------- | ---------------------------- | ------------------------------ | ------------------------------------------------ |
| **FCFS** (First-Come, First-Served)      | ❌ No       | Runs in arrival order        | Simple, fair                   | Long jobs can block short ones ("convoy effect") |
| **SJF** (Shortest Job First)             | ❌ No       | Chooses shortest job         | Minimizes average waiting time | Requires knowledge of job length                 |
| **SRTF** (Shortest Remaining Time First) | ✅ Yes      | Preemptive SJF               | Very efficient                 | Difficult to predict remaining time              |
| **RR** (Round Robin)                     | ✅ Yes      | Time-sliced (quantum-based)  | Good for time-sharing systems  | Context switching overhead                       |
| **Priority Scheduling**                  | Can be both | Chooses highest priority     | Useful in real-time systems    | Starvation possible for low-priority processes   |
| **MLQ** (Multilevel Queue)               | Depends     | Queues based on type         | Organizes jobs by category     | Rigid structure                                  |
| **MLFQ** (Multilevel Feedback Queue)     | ✅ Yes      | Jobs can move between queues | Adapts to job behavior         | Complex implementation                           |

---

## 🕹️ Key Concepts

### 🟦 Preemptive vs Non-Preemptive

- **Preemptive**: CPU can be taken away from a running process (e.g., RR, SRTF).
- **Non-preemptive**: Once a process starts, it runs to completion or blocks (e.g., FCFS, SJF).

### 🟧 Context Switching

Every time the OS switches the CPU from one process to another, it incurs overhead (saving/restoring registers, etc.).

### 🟨 Starvation & Aging

- **Starvation**: Low-priority processes never get CPU time.
- **Aging**: Gradually increasing the priority of waiting processes to prevent starvation.

---

## 📊 Example Metrics

| Metric              | Description                                 |
| ------------------- | ------------------------------------------- |
| **Turnaround Time** | Completion time – Arrival time              |
| **Waiting Time**    | Turnaround time – Burst time                |
| **Response Time**   | First run time – Arrival time               |
| **Throughput**      | Number of processes completed per unit time |

---

## 🧩 How to Choose a Scheduling Algorithm?

| System Type                     | Likely Algorithm                              |
| ------------------------------- | --------------------------------------------- |
| Batch system                    | SJF, FCFS                                     |
| Time-sharing (e.g., desktop OS) | Round Robin                                   |
| Real-time systems               | Priority-based, EDF (Earliest Deadline First) |
| Mixed workloads                 | Multilevel Feedback Queue                     |

---

## 🧠 TL;DR Summary

- **FCFS**: Simple but can lead to long wait times.
- **SJF/SRTF**: Efficient but requires knowing burst times.
- **Round Robin**: Fair and responsive, great for users.
- **Priority Scheduling**: Flexible but can cause starvation.
- **Multilevel Queues**: Good for organizing workloads.
- **MLFQ**: Smart, adaptive, and commonly used in real systems (e.g., Linux).

## Project

**Introduction:**
In this assignment, you will develop a simulation of CPU scheduling algorithms using a basic machine learning instruction set. You will implement four scheduling algorithms: Shortest Job First (SJF), First Come First Serve (FCFS), Priority Scheduling, and Round Robin. The simulation will be divided into three main components: the machine language breakdown, the scheduling algorithms, and the CPU components: ALU, Cache, and Registers.

**Machine Language Breakdown:**
The machine language instructions will form the basis of the processes that need to be scheduled. Each instruction serves a specific purpose and contributes to the execution of a process. Here is a breakdown of the instructions:

1. `ADD`: Adds the contents of two registers and stores the result in a register.
2. `LOAD`: Loads a value from memory into a register.
3. `STORE`: Stores a value from a register into memory.
4. `JUMP`: Jumps to a specified memory location.
5. `DIV`: Divides the contents of two registers and stores the quotient in a register.
6. `MOD`: Divides the contents of two registers and stores the remainder in a register.
7. `MUL`: Multiplies the contents of two registers and stores the result in a register.
8. `CALL`: Calls a subroutine or a specific memory location.
9. `HALT`: Stops the execution of a process.
10. `RET`: Returns from a subroutine.
11. `INPUT`: Accepts input from an input device and stores it in a register.
12. `OUTPUT`: Sends output to an output device.

These instructions will be executed by the CPU according to the scheduling algorithm.

**Scheduling Algorithm Explanations:**

1. **Shortest Job First (SJF):** This algorithm schedules processes based on their burst time, i.e., the amount of time required to complete the process. The process with the shortest burst time is selected next for execution.

2. **First Come First Serve (FCFS):** FCFS is a non-preemptive scheduling algorithm that executes processes in the order they arrive. The first process that enters the ready queue is the first to be executed.

3. **Priority Scheduling:** Priority scheduling assigns a priority value to each process, and the process with the highest priority is executed first. In this simulation, higher values represent higher priority.

4. **Round Robin:** Round Robin is a preemptive scheduling algorithm that assigns a fixed time quantum to each process. Each process is executed for a specified amount of time, and then it is preempted to give other processes a chance to execute.

**ALU (Arithmetic Logic Unit):**
The ALU is responsible for performing arithmetic and logical operations on data. It performs operations such as addition, subtraction, multiplication, division, modulus, and comparisons. The ALU operates on data stored in registers and updates the result accordingly.

**Cache:**
The cache is a small, fast memory located closer to the CPU than main memory. It stores frequently accessed instructions and data, providing faster access compared to main memory. Caching improves the overall performance of the CPU by reducing memory access time.

**Registers:**
Registers are small, high-speed memory units within the CPU. They hold data and instructions that are being actively used by the CPU. The registers used in this simulation include:

1. **Instruction Register (IR):** Holds the current instruction being executed.
2. **Program Counter (PC):** Stores the memory address of the next instruction to be fetched.
3. **Accumulator (AC):** Stores intermediate results of arithmetic and logical operations.
4. **General-Purpose Registers (GPR):** Provides additional storage for data and calculations.

**Conclusion:**
In this assignment, you will implement a CPU scheduling simulation using a basic machine learning instruction set. You will explore different scheduling algorithms, such as Shortest Job First, First Come First Serve, Priority Scheduling, and Round Robin. Additionally, you will simulate the key components of a CPU, including the ALU, Cache, and Registers. This assignment will help you understand the inner workings of a CPU and how scheduling algorithms impact process execution.

Remember to provide detailed explanations and implementation steps for each component, considering factors such as process arrival time, burst time, priority values, and time quantum for Round Robin.
