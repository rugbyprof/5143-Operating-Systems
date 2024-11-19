## Operating Systems Terms

### 1. Operating System Basics

- Kernel
- System Calls
- User Mode vs. Kernel Mode
- Bootstrapping/Boot Process
- Operating System Types:
  - Batch Systems
  - Time-Sharing Systems
  - Real-Time Operating Systems
  - Distributed Operating Systems
  - Embedded Systems

### 2. Process Management

- Process
- Threads
- Process States (New, Ready, Running, Waiting, Terminated)
- Process Control Block (PCB)
- Context Switch
- Multitasking
- Multiprocessing
- Multithreading
- Process Synchronization
- Inter-Process Communication (IPC)
  - Pipes
  - Message Queues
  - Shared Memory
  - Sockets

### 3. Process Scheduling

- CPU Scheduling
- Preemptive vs. Non-Preemptive Scheduling
- Scheduling Algorithms:
- First-Come, First-Served (FCFS)
  - Shortest Job Next (SJN)
  - Priority Scheduling
  - Round Robin (RR)
  - Shortest Remaining Time (SRT)
  - Multi-Level Queue Scheduling
  - Multi-Level Feedback Queue Scheduling
  - Completely Fair Scheduler (CFS)

### 4. Synchronization and Concurrency

- Critical Section
- Mutual Exclusion
- Race Conditions
- Semaphores
- Mutexes
- Monitors
- Deadlock
- Starvation
- Busy Waiting
- Condition Variables
- Spinlocks
- Atomic Operations
- Synchronization Problems:
  - Producer-Consumer Problem
  - Readers-Writers Problem
  - Dining Philosophers Problem
  - Sleeping Barber Problem

### 5. Deadlock

- Deadlock Detection
- Deadlock Prevention
- Deadlock Avoidance
- Banker’s Algorithm
- Resource Allocation Graphs
- Circular Wait
- Hold and Wait

### 6. Memory Management

- Logical Address vs. Physical Address
- Memory Allocation Techniques:
  - Contiguous Allocation
  - Non-Contiguous Allocation
- Paging
- Segmentation
- Page Tables
  - Multi-Level Page Tables
  - Inverted Page Tables
- Virtual Memory
- Page Fault
- Demand Paging
- Page Replacement Algorithms:
  - First-In-First-Out (FIFO)
  - Least Recently Used (LRU)
  - Optimal Page Replacement
  - Clock (Second-Chance) Algorithm
- Thrashing
- Fragmentation:
  - Internal Fragmentation
  - External Fragmentation

### 7. File Systems

- File Structure
- File Attributes
- File Operations
- File System Implementation
- Directory Structures:
  - Single-Level Directory
  - Two-Level Directory
  - Tree-Structured Directory
- File Allocation Methods:
  - Contiguous Allocation
  - Linked Allocation
  - Indexed Allocation
- Disk Scheduling Algorithms:
  - First-Come, First-Served (FCFS)
  - Shortest Seek Time First (SSTF)
  - SCAN/Elevator
  - Circular SCAN (C-SCAN)
  - LOOK and C-LOOK
- Journaling
- RAID Levels
- Access Control Lists (ACL)

### 8. Input/Output Management

- Device Drivers
- Device Controllers
- Interrupts
- DMA (Direct Memory Access)
- Polling
- Spooling
- Disk Structure
- Disk Scheduling Algorithms (see File Systems)

### 9. Security and Protection

- Authentication
- Authorization
- Encryption
- Access Control Mechanisms
- Discretionary Access Control (DAC)
- Mandatory Access Control (MAC)
- Role-Based Access Control (RBAC)
- Privilege Levels
- Security Threats:
  - Malware (Virus, Worm, Trojan)
  - Ransomware
  - Rootkits
  - Phishing
- System Threats:
  - Buffer Overflow
  - Denial-of-Service (DoS)
- Protection Mechanisms:
  - Firewalls
  - Intrusion Detection Systems (IDS)

### 10. Advanced Topics and Algorithms

- Virtualization
- Hypervisors
- Containerization
- Distributed Systems
- Distributed File Systems
- Remote Procedure Call (RPC)
- Distributed Synchronization
- Cloud Computing
- Real-Time Systems
- Hard vs. Soft Real-Time Systems
- Algorithms:
  - Peterson’s Algorithm
  - Lamport’s Bakery Algorithm
  - Readers-Writers Variations
  - Ricart–Agrawala Algorithm (Distributed Mutual Exclusion)
  - Bully Election Algorithm
  - Ring Election Algorithm

### 11. Networking Concepts

- Network Protocols (TCP/IP)
- Socket Programming
- Network File System (NFS)
- Remote Memory Access
- Packet Scheduling
- Fair Queuing
- Weighted Fair Queuing

### 12. Miscellaneous

- System Performance
  - Benchmarking
  - Throughput
  - Latency
- System Calls (e.g., fork, exec, wait, read, write)
- Kernel Types:
  - Monolithic Kernel
  - Microkernel
  - Hybrid Kernel
  - Exokernel
- Virtual Machines (VMs)
- Resource Allocation
- Debugging Tools (strace, gdb)
- Synchronization Hardware (Test-and-Set, Compare-and-Swap)
