```yaml
title: "Threads, Deadlocks, and Docker: Tales from the OS Trenches – Week 3"
course: "Operating Systems"
module: "Memory & File Systems"
duration: "1 week"
author: "T. Griffin / ChatGPT"
credit: "Conceptual structure and content collaboration with ChatGPT (OpenAI, GPT-5)"
```

# 🧩 Week 3: Memory & File Systems

> _“RAM is like a hotel — rooms get cleaned, but someone always forgets their toothbrush.”_

---

### 🧠 Overview

- Our spotlight shifts to **memory management** and **file systems** ... the quiet, invisible machinery that keeps processes and data alive.
- This week connects the **abstractions of virtual memory** to modern ideas like:
  - caching
  - SSD wear leveling
  - virtual disks in containers and
  - virtual machines.
- The goal is conceptual mastery: _why these systems exist_, _how they prevent chaos_, and _what happens when they fail spectacularly_.

---

### 🎯 Learning Objectives

- Describe how the OS provides each process a virtual address space.
- Explain the relationship between pages, frames, and page tables.
- Differentiate between paging, segmentation, and swapping.
- Understand caching, buffering, and the file I/O hierarchy.
- Outline the structure and purpose of a filesystem.
- Relate classical disk and memory concepts to SSDs, containers, and cloud storage.

---

### 🧩 Lecture Topics

1. **Memory Abstraction and Protection**

   - The illusion of “infinite memory.”
   - Address translation (concept only).
   - Page tables, offsets, and protection bits.

2. **Paging and Virtual Memory**

   - Pages and frames (4 KB mental model).
   - Page faults and demand paging.
   - Replacement policies: FIFO, LRU, Optimal (the mythical one).
   - Swapping and thrashing (when the OS starts to cry).

3. **Caching and Buffering**

   - Memory hierarchy and latency gaps.
   - Caches, TLBs, and prefetching in plain English.
   - Buffers and I/O queues.

4. **File Systems and Persistent Storage**

   - Hierarchical directories, inodes, blocks, and metadata.
   - Allocation strategies: contiguous, linked, indexed.
   - Journaling and crash recovery.
   - SSDs and wear leveling (why your flash drive ages badly).

5. **Modern Evolution**

   - RAM disks and tmpfs.
   - Container overlays and virtual block devices.
   - Distributed file systems (concept only: NFS, GlusterFS, etc.).

---

### 📘 Suggested Readings

- _Operating Systems: Three Easy Pieces_ — Chapters on memory, paging, and filesystems.
- Tanenbaum, _Modern Operating Systems_ — “File-System Implementation.”
- Blog post: “The Surprising Longevity of the Page Table.”
- Optional: Explore `lsblk`, `df`, and `free -h` on a Linux system for real data inspection.

---

### 💻 Project 3: **Paging and Caching Simulator**

**Goal:** Model a simplified memory manager to understand paging and replacement strategies.

**Summary:**
Simulate a process requesting pages from a limited set of memory frames.
Track page hits, faults, and replacement operations using various algorithms.

**Requirements:**

- Represent memory as a fixed-size list or array (e.g., 4 or 8 frames).
- Simulate incoming page references (either generated or read from a file).
- Implement at least two replacement policies (FIFO and LRU).
- Display statistics: total requests, hits, faults, and hit ratio.

**Optional Enhancements:**

- Add a “visual” mode showing page table and frame changes over time.
- Include a small cache layer between “RAM” and “disk.”
- Integrate timing or delay simulation to represent access cost differences.

**Deliverables:**

- Source code (`paging_simulator.py` or `.cpp`)
- Sample input and output
- Reflection on how replacement policy affects performance.

---

### 💬 Discussion Prompt

> “The OS promises every process its own private memory — but where’s the magic?”
> This discussion explores the idea that virtual memory isn’t about having _more_ RAM, but about smarter management of limited resources.

---

[◀️ Week 02: Concurrency & Synchronization](../Week_02/README.md) :: [Week 04: Modern OS & Virtualization ▶️](../Week_04/README.md)
