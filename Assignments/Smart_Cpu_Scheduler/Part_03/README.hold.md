# CPU Scheduling Simulator Assignment

## 📚 Overview

In this assignment, you'll implement and test multiple CPU scheduling algorithms in a controlled simulation environment. You'll compare their performance across various workloads and report key metrics such as average turnaround time, waiting time, response time, and CPU utilization.

## 📦 Structure

- `schedulers/`: Each scheduling algorithm goes here
- `simulator/`: Core event loop, process model, and metrics
- `configs/`: JSON files for parameter sweeps
- `results/`: Output files (CSV or JSON)
- `data/`: Process definitions
- `run_sim.py`: Entrypoint

## ✅ Requirements

Implement the following algorithms:

- [x] FCFS – First Come First Served
- [x] RR – Round Robin (configurable quantum)
- [x] SJF – Shortest Job First (non-preemptive)
- [x] SRTF – Shortest Remaining Time First (preemptive)
- [x] Priority – Static (bonus: dynamic priority aging)

## ⚙️ Config File Example

Config files are suggestions, not a requirement.

```json
{
  "scheduler": "RR",
  "quantum": 5,
  "context_switch": 1,
  "process_file": "data/sample_processes.json"
}
```

## 📅 Suggested Order

Tackle the algorithms in this order(ish)

|     | Task                                |     |
| --- | ----------------------------------- | --- |
| 1   | Implement base `Scheduler` and FCFS | ✅  |
| 2   | Add RR, SJF                         |     |
| 3   | Add SRTF, Priority                  |     |
| 4   | Batch test with config sweeps       |     |
| 5   | Report generation + write-up        |     |

## 🧪 Recommended Simulation Parameters

You want to explore _how scheduling algorithms perform under different conditions_. These parameters will give you both breadth and control over experiment design:

### **1. Number of Processes**

- Vary: `10`, `50`, `100`, `500+`
- Purpose: Scale test — how does the algorithm behave as load increases?

### **2. Arrival Times**

- Scenarios:
  - **All at t=0** (worst case for FCFS)
  - **Uniform random** between `0` and some max arrival time (e.g., 1000)
  - **Bursty arrivals** (groups of jobs arrive at similar times)

### **3. CPU Burst Characteristics**

- Use statistical distributions:
  - **Short jobs**: e.g., normal/poisson with low mean
  - **Long jobs**: same with higher mean
  - **Mixed workloads**: bimodal distribution
- Parameters: `cpu_burst_mean`, `cpu_burst_stddev`

> <sup>**SEE BELOW FOR BREAKDOWN**</sup>

### **4. I/O Behavior**

- Include:
  - `io_ratio`: proportion of time a job spends in I/O
  - `io_burst_mean` and `stddev`
- Important for SRTF, RR, and Priority (I/O-bound jobs get punished or rewarded differently)

### **5. Quantum (for Round Robin)**

- Vary: `2`, `5`, `10`, `20`
- RR is sensitive to quantum — large quantum behaves like FCFS, small quantum increases context switches

### **6. Priority Levels (for Priority scheduling)**

- Number of levels: 3, 5, or 10
- Static vs dynamic
- Random vs class-based priority (e.g., IO-heavy jobs have higher/lower priority)

### **7. Context Switch Overhead**

- Optional, but realistic
- Penalize context switches with a delay

---

## 📊 Metrics to Collect

Every simulation should collect:

| Metric                      | Why It's Important                |
| --------------------------- | --------------------------------- |
| **Average Turnaround Time** | Overall performance               |
| **Average Waiting Time**    | Fairness                          |
| **CPU Utilization**         | Efficiency                        |
| **Throughput**              | Jobs per unit time                |
| **# Context Switches**      | Cost of preemptive algorithms     |
| **Response Time (1st run)** | Interactivity (especially for RR) |

---

## 🎯 More on CPU Burst Characteristics:

- A **CPU burst** is a period when a process is actively using the CPU.
- A typical process has **multiple bursts**, interleaved with **I/O bursts**.
- The _length_ of these CPU bursts can drastically affect how different scheduling algorithms perform.

### 🎲 Using Statistical Distributions to Generate Bursts

Instead of hardcoding burst times, or a simple random number generator, we need to use **statistical distributions** to create more realistic and testable simulations.

### 🔹 **Short Jobs**

Use **distributions with a low average value**:

- **Normal (Gaussian)**:

  ```python
  random.normalvariate(mean=5, stddev=2)
  ```

  - Good for symmetrical short burst times.
  - Can sometimes generate negative values → clamp or discard them.

- **Poisson or Exponential**:
  ```python
  numpy.random.exponential(scale=5)
  ```
  - Exponential bursts mimic real-world short tasks: many small jobs, few long ones.

### 🔹 **Long Jobs**

Use the **same distributions**, but with a **higher mean**:

- Example:

  ```python
  # Simulate a CPU-bound process
  random.normalvariate(mean=20, stddev=5)
  ```

- These simulate **CPU-intensive** programs (e.g., video rendering, data processing).

### 🔀 **Mixed Workloads**

For more realistic testing, simulate a **bimodal distribution**: a mix of **short** and **long** jobs.

You can do this manually:

```python
def generate_bimodal_burst():
    if random.random() < 0.5:
        # Short job
        return int(random.normalvariate(5, 2))
    else:
        # Long job
        return int(random.normalvariate(20, 5))
```

This results in **two clusters**:

- A group of short jobs
- A group of long jobs  
  _…exactly the kind of situation where SJF and Priority schedulers shine (or fail)._

---

### 🧠 Why It Matters

Different algorithms behave **very differently** depending on the burst profile:

| Distribution | FCFS                                                 | SJF/SRTF                | RR                     |
| ------------ | ---------------------------------------------------- | ----------------------- | ---------------------- |
| Short jobs   | Penalized if behind long jobs                        | Very efficient          | Works well             |
| Long jobs    | Fine                                                 | Starved (if preemptive) | Fragmented             |
| Mixed        | Exposes weaknesses (convoy effect, starvation, etc.) | Ideal testbed           | Quantum tuning matters |

---

### 🧪 Assigning Profiles to Processes

In our JSON generator we can tell it what kind of jobs to generate:

- Assign process types: `short`, `long`, or `mixed`
- Generate CPU bursts accordingly:

```python
process_profile = random.choice(['short', 'long', 'mixed'])

if process_profile == 'short':
    bursts = [int(random.expovariate(1/5)) for _ in range(num_bursts)]
elif process_profile == 'long':
    bursts = [int(random.expovariate(1/20)) for _ in range(num_bursts)]
else:
    bursts = [generate_bimodal_burst() for _ in range(num_bursts)]
```

We can add this idea to our current job classes that is located [HERE](../../../Lectures/Smart_Cpu_Scheduler/gen_jobs/generate_jobs.py)

---

## ✅ Summary Table

| Type      | Distribution        | Mean ± StdDev | Real-World Analogy             |
| --------- | ------------------- | ------------- | ------------------------------ |
| Short Job | Normal, Exponential | 5 ± 2         | Text editor, CLI tool          |
| Long Job  | Normal, Exponential | 20 ± 5        | Compiler, video rendering      |
| Mixed     | Bimodal             | ~5 and ~20    | Shared server with varied load |

---

## 📈 Goals

- Gantt chart visualizations
- Multi-core simulation
- I/O-bound process handling
- Live visualization (pygame or matplotlib)

## 🗂️ Organizational Advice

### **1. Modular Simulation Design**

- Separate **scheduler logic** from **simulation loop**
- Use a base `Scheduler` class with:
  ```python
  class Scheduler:
      def add_process(self, process): ...
      def get_next_process(self): ...
      def tick(self): ...
  ```
  Then subclass: `FCFS`, `RR`, `SJF`, etc.

### **2. Use Config Files for Parameters**

- Let them define `.json` or `.yaml` configs:
  ```json
  {
    "num_processes": 100,
    "cpu_burst_mean": 10,
    "io_ratio": 0.3,
    "quantum": 5,
    "scheduler": "RR"
  }
  ```
- This makes reproducibility and batch runs easier.

### **3. Automate Runs with Parameter Sweeps**

Use nested `for` loops or scripts like:

```python
for algo in schedulers:
    for burst_mean in [5, 10, 20]:
        for quantum in [2, 5, 10]:
            run_sim(algo, burst_mean, quantum)
```

### **4. Export Results to CSV**

So they can:

- Graph it with pandas/Matplotlib
- Do further analysis (e.g., boxplots of turnaround time)

---

## 🎓 Stretch Goals

- Add **multi-core CPU** support (easy parallelism test)
- Add **adaptive scheduling** (e.g., aging or Linux-style hybrid)
- Visualize Gantt charts with `matplotlib` or even `pygame`
- Track **per-job stats** (not just averages)

---

---

## ✅ TL;DR Checklist

- [x] Vary: number of processes, burst lengths, arrival times
- [x] Simulate FCFS, RR, SJF, SRTF, Priority (preemptive/non)
- [x] Collect key metrics (TT, WT, RT, Utilization)
- [x] Automate runs across parameter sets
- [x] Output results to CSV + visualizations

---

Want a scaffold repo or starter template? I can generate that too.

## 📑 Rubric (100 pts)

Loosely made rubric.

| Category                     | Points |
| ---------------------------- | ------ |
| FCFS + RR implemented        | 20     |
| SJF + SRTF + Priority        | 30     |
| Working event loop           | 15     |
| Metrics collected correctly  | 10     |
| Configurable parameters      | 10     |
| Result logging (CSV/JSON)    | 5      |
| Code quality + modularity    | 5      |
| Bonus (aging, visualization) | +5     |

---

## 👨‍🏫 Notes

- You may continue working in teams of 3.
- You **must** include at least one run where all processes arrive at `t=0` for FCFS analysis.
- Plagiarism will result in a zero.

---

## 🧠 Questions to Explore

- How sensitive is RR to quantum size?
- How does I/O affect turnaround?
- Which scheduler is best for short jobs? For long ones?
- How can fairness be measured?

# BELOW HERE IS IN PROGRESS

## 🗂️ Folder Structure

Idea on how you can organize your code. We already have a `pkg` folder, but we need to organize our scheduler code as well.

```

cpu_scheduler_sim/
├── schedulers/
│ ├── **init**.py
│ ├── base_scheduler.py
│ ├── fcfs.py
│ ├── rr.py
│ ├── sjf.py
│ ├── srtf.py
│ ├── priority.py
├── simulator/
│ ├── **init**.py
│ ├── process.py
│ ├── event_loop.py
│ └── metrics.py
├── pkg/
│ ├── **init**.py
│ ├── clock.py
│ ├── cpu.py
│ ├── ioDevice.py
│ ├── process.py
│ └── scheduler.py
├── configs/
│ ├── baseline.json
│ ├── sweep_rr_quantum.json
├── data/
│ └── sample_processes.json
├── results/
│ └── results.csv
├── run_sim.py
├── analyze_results.ipynb
└── README.md

```

---

## 🧱 Class Stubs

Here are a few ideas on what methods may be helpful in a base scheduler to be extended by your specific algorithm classes.

### `schedulers/base_scheduler.py`

```python
class Scheduler:
    def __init__(self, **kwargs):
        self.ready_queue = []

    def add_process(self, process):
        raise NotImplementedError

    def get_next_process(self, current_time):
        raise NotImplementedError

    def preempt_check(self, current_process, new_process):
        return False  # Override in preemptive schedulers

    def __str__(self):
        return self.__class__.__name__
```

---

### `schedulers/fcfs.py`

Write a class for each scheduling algorithm.

```python
from .base_scheduler import Scheduler

class FCFS(Scheduler):
    def add_process(self, process):
        self.ready_queue.append(process)

    def get_next_process(self, current_time):
        if self.ready_queue:
            return self.ready_queue.pop(0)
        return None
```

_Similar files for `RR`, `SJF`, `SRTF`, `Priority` with extra logic_

---

### `simulator/process.py`

A process that keeps track of all the data needed to assess how a scheduler is doing.

```python
class Process:
    def __init__(self, pid, arrival_time, cpu_bursts, io_bursts, priority=0):
        self.pid = pid
        self.arrival_time = arrival_time
        self.cpu_bursts = cpu_bursts
        self.io_bursts = io_bursts
        self.priority = priority

        self.wait_time = 0
        self.turnaround_time = 0
        self.start_time = None
        self.response_time = None
        self.finished_time = None

    def is_done(self):
        return not self.cpu_bursts
```

---

### `simulator/event_loop.py`

Run a loop similar to what we're already doing.

```python
def run_simulation(process_list, scheduler, context_switch=0, quantum=None):
    """
    Core simulation loop
    - Feed processes to scheduler
    - Handle I/O wait queue
    - Collect performance stats
    Returns: metrics (dict)
    """
    raise NotImplementedError("You must implement the event loop.")
```

---

### `simulator/metrics.py`

If all your processes end up in the "terminated" queue, well, calculating metrics is a breeze.

```python
def compute_metrics(processes):
    """
    Aggregate metrics:
    - Avg Turnaround Time
    - Avg Wait Time
    - Avg Response Time
    - Throughput
    - Context switches
    """
    raise NotImplementedError("Metrics aggregation needed.")
```

---

### `run_sim.py`

Driver code.

```python
import json
from schedulers.fcfs import FCFS
# from schedulers.rr import RR
# ...

from simulator.process import Process
from simulator.event_loop import run_simulation

def load_processes(path):
    with open(path) as f:
        data = json.load(f)
    return [Process(**p) for p in data]

if __name__ == "__main__":
    config = json.load(open("configs/baseline.json"))
    processes = load_processes(config["process_file"])
    scheduler = FCFS()

    results = run_simulation(processes, scheduler)
    print(results)
```

---
