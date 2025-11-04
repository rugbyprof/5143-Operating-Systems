```yaml
title: "Week 1 Glossary: The World Beneath the GUI"
course: "Operating Systems"
author: "T. Griffin"
context: "Week 1 foundational terminology and concepts related to operating systems."
tags:
  [operating-systems, glossary, system-calls, scheduling, processes, threads]
```

## 🧠 Week 1 Glossary — _“The World Beneath the GUI”_

| Term                             | Definition                                                                                                                                 | Example / Analogy                                                                 |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------- |
| **Operating System (OS)**        | The software layer that manages hardware resources and provides services to programs. It decides _who gets to play with the CPU and when_. | Think of it as an air-traffic controller for your CPU, RAM, and I/O devices.      |
| **Kernel**                       | The core part of the OS that runs in **privileged (kernel) mode**. Handles scheduling, memory management, I/O, and system calls.           | The “engine room” of the OS — users don’t enter, but it keeps the ship running.   |
| **User Mode**                    | A restricted CPU mode where normal applications run. Prevents programs from directly accessing hardware.                                   | Like passengers on a plane: you can order snacks, not fly the plane.              |
| **Kernel Mode**                  | Privileged mode where the OS kernel runs. Has full access to memory and devices.                                                           | The pilot’s cockpit — no passengers allowed.                                      |
| **System Call (syscall)**        | A controlled way for user programs to request services from the kernel.                                                                    | `read()`, `write()`, `fork()`, `exec()`, and `wait()` are all syscalls.           |
| **Trap / Interrupt / Exception** | Mechanisms that switch the CPU from user mode to kernel mode in response to events or errors.                                              | A trap is a polite “excuse me”; an interrupt is someone barging into your office. |
| **Process**                      | A running instance of a program with its own memory, registers, and state.                                                                 | If a program is a recipe, a process is a chef actively cooking it.                |
| **Thread**                       | The smallest unit of CPU execution within a process. Threads share memory but run independently.                                           | Multiple cooks working from the same recipe in the same kitchen.                  |
| **Process States**               | The typical lifecycle stages: _new → ready → running → waiting → terminated._                                                              | Like a roller coaster queue: waiting, riding, pausing, done.                      |
| **Scheduler**                    | The OS component that decides which process runs next.                                                                                     | The DJ deciding which song (process) plays next.                                  |
| **Scheduling Algorithms**        | Rules for picking which process runs: **FCFS** (First Come, First Served), **SJF** (Shortest Job First), **RR** (Round Robin).             | FCFS is a line at Starbucks; RR is speed dating; SJF is “quick tasks first.”      |
| **Context Switch**               | When the CPU saves one process’s state and loads another’s. This allows multitasking.                                                      | Like bookmarking a novel before switching to another — fast, but not free.        |
| **Multithreading**               | Running multiple threads within the same process to achieve concurrency.                                                                   | One cook stirs while another chops — teamwork!                                    |
| **Concurrency**                  | Multiple tasks _making progress_ at the same time (not necessarily simultaneously).                                                        | Juggling — only one ball in hand at a time, but all are moving.                   |
| **Parallelism**                  | Actually executing multiple tasks at the _exact same time_ (needs multiple cores).                                                         | Multiple jugglers each with their own set of balls.                               |
| **Abstraction**                  | The OS hides low-level hardware details and presents simple interfaces.                                                                    | You drive a car without knowing fuel-injection details.                           |
| **Resource Management**          | Allocation of CPU, memory, storage, and I/O among competing processes.                                                                     | Like divvying up pizza slices at a party — everyone wants more.                   |
| **Isolation / Protection**       | Preventing one process from interfering with another or the kernel.                                                                        | Sandbox walls between apps — your game can’t crash your browser.                  |
| **Throughput**                   | Number of processes completed per unit time.                                                                                               | Assembly-line speed: how many widgets per hour.                                   |
| **Latency / Turnaround Time**    | Time taken for one process to finish.                                                                                                      | How long before your burger order comes out.                                      |
| **Fairness**                     | Ensuring all processes get CPU time without starvation.                                                                                    | “No one hogs the swing set.”                                                      |
| **Preemption**                   | Forcibly interrupting a running process so another can run.                                                                                | The teacher saying, “Time’s up, next student!”                                    |
| **`fork()`**                     | Creates a copy of the current process.                                                                                                     | The cell division of Unix.                                                        |
| **`exec()`**                     | Replaces the current process image with a new program.                                                                                     | Body swap — same process ID, new personality.                                     |
| **`wait()`**                     | Pauses a parent process until its child finishes.                                                                                          | A parent waiting for the kid to finish cleaning their room.                       |
| **`read()` / `write()`**         | Syscalls for reading from and writing to files or devices.                                                                                 | OS-mediated “input” and “output” — because raw hardware access is forbidden.      |
| **`strace` / `dtruss`**          | Tools to observe system calls on Linux (`strace`) or macOS (`dtruss`).                                                                     | Like eavesdropping on conversations between your app and the kernel.              |
| **Context Switch Overhead**      | The time and CPU cost to save/restore process states during a switch.                                                                      | The tax you pay for multitasking magic.                                           |

---

### 🧩 Suggested Visual Pairings

- **State Diagram** – for process transitions (`new`, `ready`, `running`, etc.).
- **CPU Timeline Chart** – to illustrate FCFS vs RR vs SJF.
- **User/Kernel Stack Diagram** – for syscall boundaries and traps.

---

### 💡 Game

- Lets role-play as the **CPU scheduler**: hand them “process cards” with burst times, and let them “schedule” themselves based on FCFS, SJF, and RR rules.
- You'll never forget context switching again — especially the one who gets preempted mid-sentence.

---

Would you like me to generate a **matching quiz** or **Anki flashcard YAML** for this glossary next? It’d pair perfectly with the Week 1 reflection and discussion prompt.
