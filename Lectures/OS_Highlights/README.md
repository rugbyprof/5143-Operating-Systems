```yaml
series: "Threads, Deadlocks, and Docker: Tales from the OS Trenches"
course: "Operating Systems"
author: "T. Griffin / Chat GPT"
weeks: 4
goal: "Give students a lively, modern understanding of OS principles through short, project-driven modules that bridge classical theory and current systems practice."
weeks:
  - id: 01
    title: "OS Foundations"
    folder: "Week_01"
  - id: 02
    title: "Concurrency & Synchronization"
    folder: "Week_02"
  - id: 03
    title: "Memory & File Systems"
    folder: "Week_03"
  - id: 04
    title: "Modern OS & Virtualization"
    folder: "Week_04"
```

# 🧩 Operating Systems Mini-Series

## **Threads, Deadlocks, and Docker: Tales from the OS Trenches**

Operating systems are the _unsung roadies_ of the computing world — tuning hardware, cueing processes, and keeping the show from crashing mid-riff.
This 3–4 week crash course introduces students to the critical concepts every computer scientist should know — **without** drowning them in page tables and hex addresses.

Instead, we’ll emphasize **how the OS thinks**, **why its abstractions matter**, and **how those concepts evolve** into modern virtualization and containerization systems.

---

## 🎯 **Series Learning Goals**

By the end of this series, you should be able to:

- Explain the OS’s role as a resource manager and abstraction layer.
- Distinguish processes, threads, and scheduling strategies.
- Recognize synchronization and deadlock problems in concurrent code.
- Describe virtual memory and file systems conceptually.
- Understand the principles behind virtualization and containerization.

---

## 🗓️ **Outline**

| Week | Focus                         | Classic Anchor                           | Modern Tie-In                   | Project                    |
| ---- | ----------------------------- | ---------------------------------------- | ------------------------------- | -------------------------- |
| 1    | OS Foundations                | CPU & I/O scheduling                     | Process simulators              | Build a “Process Zoo”      |
| 2    | Concurrency & Synchronization | Dining Philosophers, Producers/Consumers | Python `threading` / async demo | Visualize race conditions  |
| 3    | Memory & File Systems         | Paging, caching, I/O                     | Memory visualization            | Page replacement simulator |
| 4    | Modern OS & Virtualization    | Unix philosophy, kernels                 | Containers & VMs                | Lightweight container sim  |

---
