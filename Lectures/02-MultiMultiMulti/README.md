## Multiprogramming, Multiprocessing, Multitasking, and Multithreading

### Multiprogramming

- Concept of loading more than one process into memory.
- Each process ran until it blocked itself.
- Not every process fits into memory.
  - `Virtual Memory`
  - `Paging`
- Processes tend to be `CPU-Bound` or `IO-Bound`

### Multiprocessing
- Running more than one process at a time.
- Sounds like Multiprogramming, but requires more hardware (aka CPU's)
- Any system with more than one `CPU` or more than one `CORE` is Multiprocessing.

### Multitasking
- Definition seems like Multiprogramming but does have distinct differences.
  - Multiprogramming processes ran until they blocked themselves possibly hogging cpu
  - Multitasking process all run with illusion of parallelism
- Multitasking switches between each process by giving them a small amount of time to run on cpu (Time Quantum)

### Multithreading
- Allows programmer to take single process and divide it into sub-processes, running each "concurrently".
- Can reduce a processes run time.
- Sub processes typically called `Threads`
- Threads share memory space of parent process introducing new problems to manage:
  - `Race Conditions`
  - `Critical Section`
  - `Mutexes`
  - `Semaphores`


## Terms

- Time Quantum
- Virtual Memory
- CPU
- CORE
- Blocked
- Pre-Empted
- Context Switch
- IO Bound
- CPU Bound
- IO Operations
- CPU Operations
- Concurrent Processes (Threads)
- Race Condition
- Critical Section
- Mutex
- Semaphore
- Resource