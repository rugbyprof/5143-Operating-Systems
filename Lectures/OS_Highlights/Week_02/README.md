```yaml
title: "Threads, Deadlocks, and Docker: Tales from the OS Trenches – Week 2"
course: "Operating Systems"
module: "Concurrency & Synchronization"
duration: "1 week"
author: "T. Griffin / ChatGPT"
credit: "Conceptual structure and content collaboration with ChatGPT (OpenAI, GPT-5)"
```

# 🧩 Week 2: Concurrency & Synchronization

> _“Concurrency: where two threads enter, and only one leaves alive.”_

---

### 🧠 Overview

- This week explores **how multiple processes and threads interact**—and occasionally collide.
- Classical problems like **Dining Philosophers** and **Producer–Consumer** still describe the core challenges of modern parallelism.
- Even cloud-scale systems and microservices deal with the same timeless issues:
  - deadlocks
  - race conditions
  - synchronization

---

### 🎯 Learning Objectives

- Explain why concurrency exists and why it’s difficult to manage.
- Describe critical sections, mutual exclusion, and race conditions.
- Differentiate between synchronization mechanisms: mutexes, semaphores, and monitors.
- Identify and resolve deadlock and starvation scenarios.
- Connect classical concurrency models to modern multithreaded programming.

---

### 🧩 Lecture Topics

1. **The Nature of Concurrency**

   - Parallel vs. concurrent execution
   - Shared resources and nondeterminism
   - Real-world concurrency: web servers, OS schedulers, databases

2. **Critical Sections and Race Conditions**

   - Definition and examples
   - Why simultaneous access breaks consistency
   - Tools for enforcing mutual exclusion

3. **Synchronization Primitives**

   - Mutex locks and binary semaphores
   - Counting semaphores and condition variables
   - Monitors, message queues, and channels

4. **Deadlocks and Starvation**

   - Coffman’s four conditions
   - Detection vs. prevention vs. avoidance
   - Circular wait and resource ordering

5. **Classical Concurrency Problems**

   - Dining Philosophers
   - Producer–Consumer (Bounded Buffer)
   - Readers–Writers problem

6. **Concurrency in the Modern Era**

   - Threads and async I/O in Python/C++
   - Actor models and message passing
   - Concurrency inside containers and cloud systems

---

### 📘 Suggested Readings

- _Operating Systems: Three Easy Pieces_ — Chapters on concurrency and synchronization
- Dijkstra, E. W. — “Cooperating Sequential Processes” (classic short paper)
- Short video: “Why Deadlocks Still Haunt Modern Software” (YouTube or OSDev channel)

---

### 💻 Project 2: **The Hungry Philosophers Café**

**Goal:** Model a concurrent system where resource sharing can lead to deadlock and explore strategies to prevent it.

**Summary:**
Create a simulation (Python or C++) where five or more “philosophers” alternate between thinking and eating.
Each philosopher needs two shared “forks” (mutexes) to eat.
Without proper synchronization, deadlocks can occur.

**Requirements:**

- Each philosopher runs in its own thread or process.
- Use semaphores or mutexes to control resource access.
- Implement two versions:

  1. _Naïve_ version (guaranteed to deadlock eventually).
  2. _Improved_ version (e.g., resource ordering, waiter algorithm).

- Display or log each philosopher’s state: _thinking_, _hungry_, _eating_.

**Optional Enhancements:**

- Visual output using ASCII animation or a lightweight graphics library.
- Add random delays or timed “meals” to simulate unpredictable scheduling.

**Deliverables:**

- Source file(s)
- Brief write-up describing the cause and resolution of deadlock in your design.

---

### 💬 Discussion Prompt

> “In a world of perfect multitasking, do we even need synchronization?”
> Discuss how hardware evolution (multi-core CPUs, GPUs, cloud concurrency) doesn’t remove but **magnifies** the need for synchronization principles.

---

[◀️ Week 01: OS Foundations ](../Week_01/README.md) :: [Week 03: Memory & File Systems ▶️](../Week_03/README.md)
