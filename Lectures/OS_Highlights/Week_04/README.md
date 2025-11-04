```yaml
title: "Threads, Deadlocks, and Docker: Tales from the OS Trenches – Week 4"
course: "Operating Systems"
module: "Modern OS & Virtualization"
duration: "1 week"
author: "T. Griffin / ChatGPT"
credit: "Conceptual structure and content collaboration with ChatGPT (OpenAI, GPT-5)"
```

# 🧩 Week 4: Modern OS & Virtualizations

> _“Inside every container is a tiny OS screaming quietly.”_

---

### 🧠 Overview

- This final week connects everything — from the CPU scheduler to the file system — into the **modern world of virtualization and containers**.
- You will explore how an operating system can run _inside_ another OS, how containers isolate processes without full virtualization, and what it all means for scalability and security.
- The focus is conceptual fluency: understanding the **why** and **how** of virtual machines, containers, and kernel design choices.

---

### 🎯 Learning Objectives

- Explain the concept of virtualization and distinguish between full and paravirtualization.
- Describe how hypervisors create and manage virtual machines.
- Understand namespaces, cgroups, and overlay filesystems in container systems.
- Differentiate between monolithic and microkernel architectures.
- Recognize how IoT and cloud environments adapt OS principles.

---

### 🧩 Lecture Topics

1. **The Rise of Virtualization**

   - Hardware-level virtualization (Intel VT-x, AMD-V).
   - Hypervisors: Type 1 (bare-metal) vs. Type 2 (hosted).
   - Guest OS and host OS interactions.
   - Virtual I/O and resource scheduling.

2. **Containers: Virtualization’s Lightweight Cousin**

   - Process isolation using namespaces.
   - Resource limits with cgroups.
   - Overlay filesystems (AUFS, overlayfs).
   - Images, layers, and the concept of immutability.
   - The “Docker moment”: why it changed DevOps forever.

3. **Kernel Architectures and Design Trends**

   - Monolithic, microkernel, hybrid.
   - Case studies: Linux, Windows NT, MINIX, seL4.
   - Message passing vs. shared memory.
   - Trade-offs: performance, complexity, and maintainability.

4. **OS for the Edge and Cloud**

   - Minimalist OSes for containers (Alpine, CoreOS).
   - Serverless computing and function isolation.
   - OS constraints in IoT and embedded systems (FreeRTOS, Zephyr).

5. **Security and Virtual Boundaries**

   - Sandboxing, jail environments, and user namespaces.
   - Common vulnerabilities in container environments.
   - Why security isolation is an OS’s oldest problem.

---

### 📘 Suggested Readings

- _Operating Systems: Three Easy Pieces_ — Virtualization and Isolation sections.
- _The Docker Book_ (James Turnbull) — selected chapters on containers.
- Research highlight: “A Decade of Containers: Lessons Learned from Linux Namespaces.”
- Optional: Try running `docker run alpine echo "Hello from inside a container"` on a lab machine or VM.

---

### 💻 Project 4: **Build-a-Container (Mini Virtualization Lab)**

**Goal:** Demonstrate process isolation, resource limits, and layered filesystems through a simplified container simulation.

**Summary:**
Create a “container” environment using subprocesses and restricted directories.
Simulate how containers isolate processes and file systems without full hardware virtualization.

**Requirements:**

- Use a script (Python or C++) to launch subprocesses in isolated directories.
- Restrict file access to a sandbox folder.
- Simulate CPU or memory limits (e.g., delayed loops or counters).
- Optionally, use Linux tools like `chroot`, `unshare`, or `cgroups` (demo-only).
- Print environment details to show isolation success (process IDs, current path, etc.).

**Optional Enhancements:**

- Implement “layered” directories (base image + overlay folder).
- Add a logging system to monitor resource usage.
- Include container lifecycle commands: `start`, `stop`, `inspect`.

**Deliverables:**

- Source code (`mini_container.py` or `.cpp`)
- Output demonstrating isolation (directory and PID differences).
- Reflection on how containers differ from VMs in structure and purpose.

---

### 💬 Discussion Prompt

> “Is a container just a fancy process, or is it something more?”
> This discussion explores the blurred line between operating systems, runtimes, and infrastructure in the age of virtualization and microservices.

---

### 🧩 Optional Capstone Reflection

**Prompt:**

- Imagine you’re designing a new OS for a small IoT platform.
- What minimal features from the past four weeks would you include, and which would you omit?
- Justify your choices in 2–3 paragraphs, focusing on constraints, concurrency, and control.

---

[◀️ Week 03: Memory & File Systems](../Week_03/README.md)
