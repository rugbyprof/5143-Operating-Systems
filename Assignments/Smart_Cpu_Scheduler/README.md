---
title: "OS Project: Smarter CPU Scheduler"
course: "Operating Systems"
author: "T. Griffin"
due_date: "TBD"
---

# 🧩 Operating Systems Project: Building a Smarter CPU Scheduler

## Basic objectives

These are typical cpu scheduling objectives

- Understand CPU and I/O burst patterns
- Compare classical scheduling algorithms
- Design and test an adaptive scheduler
- Analyze scheduling performance metrics

## 🎯 Main Objective

Simulate CPU scheduling under realistic workloads, then design an adaptive ("learning") scheduler that improves performance compared to traditional algorithms.

---

## 1️⃣ Background

Each process behaves differently:

- **CPU-bound**: long bursts, rare I/O
- **I/O-bound**: short CPU bursts, frequent waits
- **Interactive**: tiny bursts, constant input/output
- **Mixed**: somewhere in between

Schedulers must juggle **throughput**, **latency**, and **fairness** — no single algorithm wins everywhere.

---

## 2️⃣ Phase 1 – Baseline Scheduling

Implement two traditional schedulers:

- **FCFS (First-Come, First-Served)** – simple queue, non-preemptive
- **Round Robin (RR)** – adds time slicing (quantum)

For each run, measure and log:

- Average waiting and turnaround time
- CPU utilization
- Throughput
- Response time (especially for interactive jobs)

---

## 3️⃣ Phase 2 – Smarter Algorithms

Add **SJF**, **SRTF**, and **Priority** scheduling.

Observations:

- SJF assumes you can predict burst times (spoiler: you can’t)
- Priorities can starve low-priority jobs
- Interactive processes hate long queues

---

## 4️⃣ Phase 3 – The Adaptive “Learning” Scheduler

Build a scheduler that **learns** job behavior during runtime:

- Tracks each process’s average CPU burst and I/O ratio
- Classifies it as _CPU-heavy_, _I/O-heavy_, or _interactive_
- Adjusts time slices or priorities dynamically

Example heuristic:

```text
if process is interactive → shorter quantum
if process is CPU-heavy → longer quantum
```

Optional: train a simple ML classifier (e.g., decision tree) on burst history.

---

## 5️⃣ Workload Generation

Use the provided **JSON workload generator** to create realistic process sets.

Each process looks like:

```json
{
  "pid": 17,
  "cpu_burst_mean": 30,
  "cpu_burst_stddev": 10,
  "io_profile": { "io_types": ["DISK_READ"], "io_ratio": 0.5 },
  "priority": 2,
  "interactive": false
}
```

Jobs alternate between CPU and I/O bursts until their lifetime ends.
Simulate hundreds of processes drawn from user classes like:

- **A:** Disk-heavy
- **B:** Interactive console
- **C:** Network chatty
- **D:** Mixed workloads

---

## 6️⃣ Phase 4 – Simulation & Logging

Your simulation tracks:

- Ready queue
- Waiting (I/O) queue
- CPU and I/O device activity
- Global clock (shared across system components)

Each tick, update:

- CPU bursts
- I/O bursts
- Queue movements

Export results to CSV/JSON for analysis.

---

## 7️⃣ Deliverables

1. **Code**

   - Scheduler implementations: FCFS, RR, SJF, Priority, Adaptive
   - Workload generator (JSON output)

2. **Output files**

   - Simulation timeline (CSV or JSON)
   - Graphs of throughput, latency, and fairness

3. **Report (2–3 pages)**

   - Describe your learning strategy
   - Compare results vs. RR and FCFS
   - Include at least one visualization (Gantt or state diagram)

---

## 💾 Suggested Folder Layout

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

## 🧱 Code Snippets & Stubs

### 🧩 scheduler_base.py

```python
class SchedulerBase:
    """Abstract base for all schedulers."""
    def __init__(self, ready_queue, clock):
        self.ready_queue = ready_queue
        self.clock = clock

    def add_process(self, process):
        """Insert process into queue."""
        raise NotImplementedError("Subclass must implement add_process()")

    def get_next_process(self):
        """Decide which process runs next."""
        raise NotImplementedError("Subclass must implement get_next_process()")
```

🗯 _“If you can’t decide who runs next, your OS has achieved perfect fairness: nobody runs.”_

---

### ⚙️ process.py

```python
class Process:
    """Simple representation of a process/job."""
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

---

### 🕰 clock.py

```python
class BorgClock:
    """Shared global timekeeper — the Borg clock."""
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        self.time = getattr(self, "time", 0)

    def tick(self):
        self.time += 1
        return self.time
```

💬 _“All instances share the same time — resistance is futile.”_

---

### ⚗️ workload_generator.py

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

### 🧠 Adaptive Heuristic

```python
def classify_process(history):
    """Simple heuristic to adjust quantum based on CPU/I/O behavior."""
    cpu_ratio = history["cpu_time"] / max(1, history["total_time"])
    if cpu_ratio > 0.75:
        return "CPU-heavy"
    elif cpu_ratio < 0.25:
        return "I/O-heavy"
    return "Balanced"
```

---

<details>
<summary>💡 Hint: How to Calculate Turnaround Time</summary>

Turnaround time = finish time − arrival time
Waiting time = turnaround − total CPU burst
Response time = first run − arrival

</details>

---

## 🎛️ Visualization

| Element                 | Description                   | Visualization                   |
| ----------------------- | ----------------------------- | ------------------------------- |
| **Borg Clock**          | Global simulated time         | Live clock counter              |
| **CPU Queue**           | Currently running process(es) | Highlighted in yellow           |
| **Ready Queue**         | Waiting for CPU               | Green list                      |
| **IO Queue**            | Waiting for I/O completion    | Blue list                       |
| **Exit Queue**          | Completed processes           | Gray list                       |
| **Scheduler Decisions** | Which process was chosen next | Flash message / arrow animation |

---

## 🧩 Integration Structure

You can use `rich.live` + `rich.table` + `rich.layout` to update the screen in real time every tick.

### File: `rich_scheduler_visual.py`

```python
#!/usr/bin/env python3
"""
rich_scheduler_visual.py
------------------------
Visualize the Borg-clock-driven CPU scheduler (traditional or RL-based)
using the rich library.
"""

from rich.console import Console
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from time import sleep
import random

# Assume these come from your simulation
from borg_clock import BorgClock
from cpu_scheduler_env import CPUSchedulingEnv
from stable_baselines3 import PPO

# ------------------------------------------------------------
# Initialize Environment and Model
# ------------------------------------------------------------
with open("generated_processes.json", "r") as f:
    import json
    processes = json.load(f)

env = CPUSchedulingEnv(processes)
model = PPO.load("scheduler_rl_model")

clock = BorgClock()
console = Console()

# ------------------------------------------------------------
# Visualization Helpers
# ------------------------------------------------------------
def make_queue_table(title, queue, color):
    table = Table(title=title, style=color, show_lines=True)
    table.add_column("PID", justify="center")
    table.add_column("Burst", justify="right")
    table.add_column("I/O Ratio", justify="right")
    table.add_column("Wait", justify="right")

    for p in queue:
        table.add_row(str(p["pid"]),
                      str(p["cpu_burst_mean"]),
                      f"{p['io_ratio']:.2f}",
                      str(p["wait_time"]))
    return table

# ------------------------------------------------------------
# Live Visualization Loop
# ------------------------------------------------------------
def run_visual_simulation():
    obs = env.reset()
    done = False
    total_reward = 0

    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3),
    )

    with Live(layout, refresh_per_second=5, console=console, screen=True):
        while not done:
            # Scheduler (RL model) picks next action
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, done, info = env.step(int(action))
            total_reward += reward

            clock.tick()
            cpu_table = make_queue_table("CPU Queue", [env.processes[int(action)]], "yellow")
            ready_table = make_queue_table("Ready Queue", env.ready_queue, "green")
            footer_text = Text(f"Borg Clock: {clock.time} | Reward: {reward:.2f}", style="bold cyan")

            layout["header"].update(Panel(Text("🧠 Graylian RL Scheduler Visualization", justify="center", style="bold magenta")))
            layout["body"].update(Layout())
            layout["body"].split_row(
                Layout(cpu_table, name="cpu", ratio=1),
                Layout(ready_table, name="ready", ratio=2)
            )
            layout["footer"].update(Panel(footer_text))

            sleep(0.3)

    console.print(f"\n🏁 Simulation complete! Total reward: {total_reward:.2f}", style="bold green")

# ------------------------------------------------------------
if __name__ == "__main__":
    run_visual_simulation()
```

---

## 🧠 What Students See

When running:

```bash
python rich_scheduler_visual.py
```

They’ll see something like:

```
🧠 Graylian RL Scheduler Visualization
-------------------------------------
CPU Queue: PID 3 | Burst 7 | Wait 0
Ready Queue:
 ├── PID 1 | Burst 12 | Wait 14
 ├── PID 2 | Burst 5  | Wait 7
 └── PID 4 | Burst 8  | Wait 0
-------------------------------------
Borg Clock: 37 | Reward: -6.33
```

Each tick, the RL model decides the next process, the Borg clock advances, and queues update in real-time.

---

## 🎓 Teaching Tie-Ins

| Concept              | Visual Tie                                           |
| -------------------- | ---------------------------------------------------- |
| Ready/Waiting queues | Color-coded Rich tables                              |
| Scheduling decision  | CPU panel highlights process chosen by the model     |
| Clock ticks          | Students see how simulation advances                 |
| Reward signal        | Shows the agent’s “learning feedback”                |
| Comparison mode      | Can easily switch to traditional scheduler (SJF, RR) |

---

## ⚙️ Next-Level Ideas

- Add **I/O queue animations**: processes move from ready → I/O → ready
- Use **different panels per device** (CPU, Disk, Network)
- Show **cumulative performance metrics** in a sidebar (throughput, wait avg, etc.)
- Toggle between **ML model** and **classical algorithm** via CLI flag (`--mode RL` / `--mode FCFS`)

---

## 🤓 Final Thoughts

Remember:

> _SJF is great if you can predict the future._ > _Round Robin is fair — equally slow for everyone._ > _Your learning scheduler? Maybe the first one that actually learns from its mistakes._
