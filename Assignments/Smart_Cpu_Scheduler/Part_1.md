# 🧠 Operating Systems Project – Part-1️

### Due: Sunday Night the 26th of October before Midnight

### Adding Arrival Times & Quantum Countdown

## 📘 Overview

Up to this point, our schedulers have been operating in a perfect world —  
every process magically exists at time `0`, and the CPU always has something ready to run.

**Real systems don’t work that way.**

Processes **arrive over time**, and the CPU scheduler must handle that dynamic workload fairly and efficiently.

This assignment expands your process model and scheduler logic to support:

1. **Arrival Times** — processes only enter the Ready Queue when the system clock reaches their `arrival_time`.
2. **Quantum Countdown** — each process has a time slice (quantum) used for **Round Robin** scheduling.

---

## 🧩 Task 1: Arrival Time

### 🔍 Problem

- Currently, all processes are inserted into the ready queue at startup.
- We need to make them “arrive” at different times based on an `arrival_time` attribute.
- Before you start altering arrival times, read this: [ArrivalTimeControl](./ArrivalControl.md)

### 🛠️ What to Do

- Modify your **process generation code** (e.g., `generate_processes.py` or equivalent) to include a random or defined `arrival_time` value.
  ```json
  {
    "pid": "P1",
    "arrival_time": 5,
    "cpu_burst": 8,
    "io_burst": 12,
    ...
  }
  ```
- Update your **scheduler loop** to check:
  ```python
  if clock == process.arrival_time:
      ready_queue.append(process)
  ```
- Processes should only move into the Ready Queue when the **global clock** (your Borg clock, or any global timer) equals their arrival time.

### 🧠 Hint

Arrival times don’t need to be unique — multiple processes can arrive on the same tick. Make sure your loop or dispatcher can handle that gracefully.

---

## 🧩 Task 2: Quantum Countdown (Round Robin Prep)

### 🔍 Problem

Round Robin (RR) scheduling divides CPU time into fixed-size units called **quanta**.  
A process can only execute for one quantum before being preempted.

### 🛠️ What to Do

- Add a `quantum` field to each process (either fixed globally or defined per-process).
  ```python
  process.quantum = 4  # example value
  ```
- During CPU execution:
  - Decrease the process’s remaining quantum each tick.
  - If the quantum reaches zero **and** the process is not finished:
    - Move it back into the **Ready Queue**.
    - Reset its quantum for the next round.
- Keep your `cpu_burst` countdown logic intact — a process still terminates normally when its CPU burst is done.

### 🧠 Hint

You can implement Round Robin simply by layering this countdown on top of your FCFS logic.  
If you finish both features, experiment with both `FCFS` and `RR` using the same code structure.

---

## ⏱️ Suggested Clock Loop

```python
while not all_processes_terminated:
    clock.tick()

    # 1. Move newly arrived processes into the ready queue
    for process in process_list:
        if process.arrival_time == clock.time:
            ready_queue.enqueue(process)

    # 2. Handle running process quantum
    if cpu.is_busy():
        running_process.quantum -= 1
        running_process.cpu_burst -= 1

        if running_process.cpu_burst <= 0:
            cpu.finish_process()
        elif running_process.quantum <= 0:
            cpu.preempt_process()
```

---

## 📊 Deliverables

| Item                   | Description                                                                                   |
| ---------------------- | --------------------------------------------------------------------------------------------- |
| `process_generator.py` | Updated to include `arrival_time` and `quantum` fields.                                       |
| `scheduler.py`         | Logic modified to handle arrivals and quantum countdown.                                      |
| Output / Log           | Must show process arrivals, CPU assignments, quantum expirations, and terminations over time. |

---

## 🧩 Bonus Challenges (Optional)

- Make `arrival_time` distribution configurable (e.g., Gaussian, uniform, bursty arrivals).
- Add a **Gantt Chart** or textual timeline of process execution.
- Use different quantum sizes and compare CPU utilization.

---

## 🏁 Final Notes

This is where your scheduler starts to feel _alive_ —  
processes appear, run, wait, preempt, and finish in real simulated time.

Keep your display or logs clean and chronological.  
If you already have an **Arcade visualization** running, now’s the perfect time to sync it with your clock —  
watch new processes slide into the Ready Queue as they arrive!

**⚙️ “Remember: A CPU never sleeps — it just waits for better scheduling.”**

---
