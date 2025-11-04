<!-- ```yaml
title: "The World Beneath the GUI – Week 1"
course: "Operating Systems"
module: "OS Foundations "
duration: "1 week"
author: "T. Griffin / ChatGPT"
marp: true
theme: default
paginate: true
footer: "T. Griffin — Scheduling & Context Switching (scaffolding with OpenAI GPT-5)"
``` -->

# 🧠 Week 1: The World Beneath the GUI

> “You don’t really appreciate your OS until it forgets how to boot.”

### 🧩 Overview

- In this first module, we will demystify the OS’s role: it’s not magic, just a **very clever middleman** between humans, programs, and hardware.
- We’ll model processes, scheduling, and the OS’s basic responsibilities using small simulations — the kind that make abstract ideas click.

---

### 🎯 Learning Objectives

By the end of Week 1, you should be able to:

- Define the core functions of an operating system.
- Explain the difference between user mode and kernel mode.
- Describe how processes and threads are managed by the scheduler.
- Understand the concept of system calls and context switching.

---

### 🧩 Lecture Topics

1. **What is an OS really doing?**

   - Resource management: CPU, memory, I/O.
   - Abstraction: hiding hardware complexity.
   - Protection and isolation: keeping your game from crashing your OS.

2. **Processes and Threads**

   - Lifecycle: new → ready → running → waiting → terminated.
   - States and transitions.
   - Multithreading: how the OS makes “parallel” happen.

3. **Scheduling and Context Switching**

   - FCFS, SJF, RR (conceptual only).
   - Trade-offs: throughput, latency, fairness.
   - The cost of switching (and why it matters).

4. **System Calls and the Kernel Boundary**

   - `read()`, `write()`, `fork()`, `exec()`, `wait()`.
   - Why we can’t just “call the hardware” directly.

### Summary Table

| File No. | Subtopic Title                            | Core Focus                                                            | Natural Deliverable                                        |
| -------- | ----------------------------------------- | --------------------------------------------------------------------- | ---------------------------------------------------------- |
| **001**  | **What is an OS Really Doing?**           | OS as resource manager, abstraction layer, protector                  | Intro lecture + context setting slides                     |
| **002**  | **Processes and Threads**                 | Processes vs threads, states, system calls, `fork`/`exec`             | Slide deck + small lab (“Process Zoo”)                     |
| **003**  | **Scheduling and Context Switching**      | Scheduling algorithms, fairness, pre-emption, context switch overhead | Slide deck + scheduler visualization                       |
| **004**  | **System Calls & User/Kernel Boundaries** | Interface between user space and kernel, traps, modes, security rings | Brief lecture + demo showing `strace` or `syscall` tracing |

---

### 🧰 Helpful Sources

- _Operating Systems: Three Easy Pieces_ — Chapters 1–3 (Free online)
- Short videos: “How the Kernel Schedules Your Apps” (YouTube)
- Optional: Linux man pages (`man 2 fork`, `man 2 execve`)

---

### 💻 Project: Smart Cpu Scheduler

We're already working on this [HERE](../../../Assignments/Smart_Cpu_Scheduler/README.md).

**Goal:** Visualize the life of processes competing for CPU time.

**Brief:**
Write a Python (or C++) program that:

- Simulates N processes with random burst/IO times.
- Displays process states (`ready`, `running`, `waiting`) in real-time.
- Uses time-slicing to imitate Round Robin scheduling.
- Logs context switches and total completion time. -->

**Stretch goal:** Add color-coded console output or simple GUI (e.g., `rich` or `pygame`) to make transitions visible.

**Deliverables:**

- Source code (`process_zoo.py` or `.cpp`)
- Screenshot or short demo video
- Reflection: 3–5 sentences on how the OS juggles competing tasks.

---

### 🧩 Discussion Prompt

> “If your OS could talk, how would it describe its job in one sentence?”
> Write a single-sentence “OS motto” (humor encouraged). Examples:

- “I schedule, therefore I am.”
- “Threads come and threads go — I just keep switching.”
- “When in doubt, fork yourself.”

---

## 📚 References & Credits

> **topic:** "Operating Systems Week 1 Lecture Slides"
> **focus:** "System Calls & User/Kernel Boundaries"
> **format:** "Markdown-based slide content"
> **author:** "T. Griffin and OpenAI GPT-5"
> **credit:** "Concept scaffolding with ChatGPT (OpenAI GPT-5)"

[Week 02: Concurrency & Synchronization ▶️](../Week_02/README.md)
