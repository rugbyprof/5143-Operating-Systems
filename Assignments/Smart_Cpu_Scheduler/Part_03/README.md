---

title: "OS Project: Smarter CPU Scheduler"
course: "Operating Systems"
author: "T. Griffin"
due_date: "TBD"
---------------

# 🤩 OS Project: Smarter CPU Scheduler

## 🔍 Objectives

* Understand CPU and I/O burst patterns
* Compare classical scheduling algorithms
* Design and test an adaptive scheduler
* Analyze performance metrics (e.g., wait time, turnaround)

---

## 1️⃣ Background

Each process behaves differently:

- **CPU-bound**: long bursts, rare I/O
- **I/O-bound**: short CPU bursts, frequent I/O
- **Interactive**: very short bursts, frequent input/output
- **Mixed**: balanced profile

Schedulers must juggle **throughput**, **latency**, and **fairness**.

---

## 2️⃣ Phase 1 — Baseline Schedulers

Implement two baseline schedulers:

- **FCFS**: First-Come, First-Served (non-preemptive)
- **RR**: Round Robin (preemptive, time slice)

For each run, log:

- Avg. wait time
- Avg. turnaround time
- CPU utilization
- Response time
- Throughput

---

## 3️⃣ Phase 2 — Smarter Classical Algorithms

Implement:

- **SJF**: Shortest Job First (non-preemptive)
- **SRTF**: Shortest Remaining Time First (preemptive)
- **Priority**: Static priority-based (bonus: aging)

Observe:

- Starvation risk (SJF, Priority)
- Sensitivity to burst prediction
- Interactive job performance

---

## 4️⃣ Phase 3 — Adaptive Scheduler

Design a dynamic scheduler that adjusts behavior based on runtime metrics:

- Monitor per-process stats (burst avg, I/O ratio)
- Classify as CPU-heavy, I/O-heavy, or interactive
- Dynamically assign:

  - Quantum sizes
  - Priority levels

### Example heuristic:

```text
If process is interactive → shorter quantum
If CPU-heavy → longer quantum
```

Bonus: Use ML (e.g., decision tree) to learn classifications.

---

## 5️⃣ Workload Generation

Use provided JSON generator to simulate real-world jobs.

Each class (A–D) has burst patterns:

- A: Disk-heavy
- B: Interactive (console I/O)
- C: Network chatty
- D: Mixed profile

### Sample JSON:

```json
{
  "class_id": "C",
  "cpu_burst_mean": 6,
  "cpu_burst_stddev": 2,
  "cpu_budget_mean": 40,
  "io_profile": {
    "io_types": ["SOCKET_READ", "SOCKET_WRITE"],
    "io_ratio": 0.5,
    "io_duration_mean": 15
  },
  "arrival_rate": 0.3
}
```

---

## 6️⃣ Phase 4 — Simulation Loop

Build a tick-based simulation engine with:

- Shared **BorgClock**
- Ready, I/O, and exit queues
- CPU and I/O activity
- Queue transitions per tick

Export:

- JSON/CSV timeline
- Per-process metrics

---

## 7️⃣ Deliverables

1. **Code**

   - Scheduler classes: FCFS, RR, SJF, Priority, Adaptive
   - Workload generator

2. **Output Files**

   - Simulation logs
   - Graphs (Gantt/state diagram)

3. **Report (2–3 pages)**

   - Learning strategy explanation
   - Comparative performance results
   - At least 1 visualization

---

## 💾 Suggested Directory Structure

```
Assignments/
└── OS_Scheduler/
    ├── README.md
    ├── starter_code/
    │   ├── scheduler_base.py
    │   ├── process.py
    │   ├── workload_generator.py
    │   └── utils/
    │       ├── clock.py
    │       └── logger.py
    └── examples/
        ├── fcfs_demo.json
        ├── rr_demo.json
        └── sample_output.csv
```

---

## 🧰 Code Stubs

### scheduler_base.py

```python
class SchedulerBase:
    def __init__(self, ready_queue, clock):
        self.ready_queue = ready_queue
        self.clock = clock

    def add_process(self, process):
        raise NotImplementedError()

    def get_next_process(self):
        raise NotImplementedError()
```

### process.py

```python
class Process:
    def __init__(self, pid, bursts):
        self.pid = pid
        self.bursts = bursts
        self.state = "NEW"
        self.current_burst = 0

    def next_burst(self):
        if self.current_burst < len(self.bursts):
            return self.bursts[self.current_burst]
        return None
```

### clock.py

```python
class BorgClock:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        self.time = getattr(self, "time", 0)

    def tick(self):
        self.time += 1
        return self.time
```

---

## 🕹️ workload_generator.py

```python
import random, json

def generate_process(pid, mean, stddev, io_ratio):
    return {
        "pid": pid,
        "cpu_burst_mean": mean,
        "cpu_burst_stddev": stddev,
        "io_ratio": io_ratio,
        "bursts": [abs(int(random.gauss(mean, stddev))) for _ in range(5)]
    }

if __name__ == "__main__":
    processes = [generate_process(i, 30, 10, 0.3) for i in range(10)]
    with open("workload.json", "w") as f:
        json.dump(processes, f, indent=4)
```

---

## 🤔 Heuristic Example

```python
def classify_process(history):
    cpu_ratio = history["cpu_time"] / max(1, history["total_time"])
    if cpu_ratio > 0.75:
        return "CPU-heavy"
    elif cpu_ratio < 0.25:
        return "I/O-heavy"
    return "Balanced"
```

---

## 📈 Turnaround Time Refresher

- **Turnaround Time** = Finish Time - Arrival Time
- **Waiting Time** = Turnaround - Total CPU Burst
- **Response Time** = First Run - Arrival

---

## 🎓 Summary

This project simulates realistic scheduling and challenges you to build something smarter than RR and FCFS. You'll explore tradeoffs between fairness, throughput, and latency, and test whether adaptation leads to better overall performance.
