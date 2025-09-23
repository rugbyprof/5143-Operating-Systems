# 🖥️ Lecture: Introduction to CPU Scheduling

## 1. Why Scheduling?

- A CPU can only execute one process at a time (ignoring multi-core for now).
- The **scheduler** decides which process in the ready queue gets the CPU next.
- Goals:
  - Maximize CPU utilization
  - Maximize throughput (processes completed per unit time)
  - Minimize turnaround time, waiting time, response time
  - Ensure fairness

---

## 2. Key Terms

- **Arrival Time (AT):** When a process enters the ready queue
- **Burst Time (BT):** How long the process needs CPU time
- **Waiting Time (WT):** Time spent in the ready queue
- **Turnaround Time (TAT):** Completion time – Arrival time
- **Response Time (RT):** Time until the first CPU allocation

<img src="https://images2.imgbox.com/c5/84/6aB8HC4K_o.png" width="400">

Formulas you’ll reuse:

- `TAT = CT – AT`
- `WT = TAT – BT`

---

## 3. Example Process Set

We’ll use this set throughout:

| Process | Arrival Time | Burst Time |
| ------- | ------------ | ---------- |
| P1      | 0            | 5          |
| P2      | 1            | 3          |
| P3      | 2            | 8          |
| P4      | 3            | 6          |

---

## 4. Scheduling Algorithms

### a) First-Come, First-Served (FCFS)

- Non-preemptive, processes served in arrival order.
- Think: like a queue at a bank.

**Gantt Chart:**  
`P1 | P2 | P3 | P4`  
`0   5    8   16   22`

**Turnaround & Waiting:**

| Process | CT  | TAT = CT-AT | WT = TAT-BT |
| ------- | --- | ----------- | ----------- |
| P1      | 5   | 5           | 0           |
| P2      | 8   | 7           | 4           |
| P3      | 16  | 14          | 6           |
| P4      | 22  | 19          | 13          |

Average WT = 5.75, Avg TAT = 11.25

---

### b) Shortest Job First (SJF, non-preemptive)

- Pick the process with the smallest burst time.
- Reduces average waiting time (provably optimal).

**Step-through:**

- At t=0 → P1 (BT=5)
- At t=5 → Ready: P2(3), P3(8), P4(6) → Pick P2
- At t=8 → Ready: P3(8), P4(6) → Pick P4
- At t=14 → P3(8)

**Gantt Chart:**  
`P1 | P2 | P4 | P3`  
`0   5    8   14  22`

**Results:**

| Process | CT  | TAT | WT  |
| ------- | --- | --- | --- |
| P1      | 5   | 5   | 0   |
| P2      | 8   | 7   | 4   |
| P4      | 14  | 11  | 5   |
| P3      | 22  | 20  | 12  |

Avg WT = 5.25, Avg TAT = 10.75

---

### c) Priority Scheduling

- Each process has a priority number (smaller = higher priority).
- Could be **preemptive** or **non-preemptive**.
- Example: Assign priorities: P1=2, P2=1, P3=3, P4=2.

**Non-preemptive Gantt:**  
Order = P2 → P1 → P4 → P3

---

### d) Round Robin (RR)

- Each process gets a **time quantum** (say q=4).
- Preemptive: if process not done, put it at the end of the queue.

**Walkthrough with q=4:**

- t=0: P1 runs 4/5 (1 left)
- t=4: P2 runs 3/3 (done at 7)
- t=7: P3 runs 4/8 (4 left)
- t=11: P4 runs 4/6 (2 left)
- t=15: P1 runs 1/1 (done)
- t=16: P3 runs 4/4 (done)
- t=20: P4 runs 2/2 (done)

**Gantt Chart:**  
`P1 | P2 | P3 | P4 | P1 | P3 | P4`  
`0   4    7   11  15  16  20  22`

(You can calculate WT and TAT step-by-step in class.)

---

## 5. Wrap-up

- **FCFS:** Simple, but can cause **convoy effect**.
- **SJF:** Optimal for avg. waiting, but hard to predict burst times.
- **Priority:** Flexible, but can starve low-priority jobs.
- **RR:** Good for fairness and time-sharing, but performance depends on quantum.

---

Would you like me to also make **ready-to-use slides (markdown with diagrams)** so you can just plug them into your lecture, or keep this as a lecture note with walkthrough tables?





