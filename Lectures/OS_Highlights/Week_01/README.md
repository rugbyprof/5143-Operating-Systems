```yaml
title: "Threads, Deadlocks, and Docker: Tales from the OS Trenches – Week 3"
course: "Operating Systems"
module: "OS Foundations "
duration: "1 week"
author: "T. Griffin / ChatGPT"
credit: "Conceptual structure and content collaboration with ChatGPT (OpenAI, GPT-5)"
```

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

[Week 02: Concurrency & Synchronization ▶️](../Week_02/README.md)
