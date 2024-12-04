## CPU Scheduling Experimental Runs

Below, are lists of categories and parameter values organized such that you can generate experiments by selecting subsets of the provided information. This can be done randomly or with some organized progression.

I have a new term I call `RTP` or Random Threshold Pairs that are really min/max values in which random values can be generated between. It was easier to get good data from chat gpt for my categories and required parameters when the question is stated scientifically. Anyway, below are lists for each category, with explanations of how they align with a specified behavior (e.g., heavy CPU, heavy IO, Large Quantum, Small ... you get it). For each list, I’ve ensured the values are statistically plausible and flexible enough for a broad range of experimentation.

### 1. RTP Pairs for CPU vs. IO-Heavy Processes

**Goal:**

Traverse the spectrum from CPU-heavy processes (long burst times, little IO) to IO-heavy processes (short burst times, frequent IO).

**RTP List:**

| Scenario             | Burst Time RTP | IO Frequency RTP | IO Duration RTP |
| -------------------- | -------------- | ---------------- | --------------- |
| Moderately CPU-heavy | (20, 60)       | (2, 4)           | (2, 8)          |
| Balanced             | (10, 30)       | (5, 10)          | (5, 15)         |
| Moderately IO-heavy  | (5, 15)        | (10, 15)         | (10, 20)        |
| Very IO-heavy        | (1, 5)         | (15, 20)         | (15, 30)        |

**- Explanation**:

- `Burst Time RTP`: Longer values indicate heavy CPU processes.
- `IO Frequency RTP`: Frequency is modeled as “number of IO requests per burst.”
- `IO Duration RTP`: Represents the time spent on IO operations.

### 2. RTP Pairs for Time Quantum in RR

**Goal:**

Explore the effect of quantum size on performance, from very small (high preemption) to very large (mimicking FCFS).

**RTP List:**

| Scenario           | Quantum RTP |
| ------------------ | ----------- |
| Very small quantum | (1, 5)      |
| Small quantum      | (5, 10)     |
| Moderate quantum   | (10, 20)    |
| Large quantum      | (20, 50)    |
| Very large quantum | (50, 100)   |

**- Explanation**:

- `Smaller quanta` force frequent context switching (good for short jobs but penalizes longer ones).
- `Larger quanta` reduce context switching but may increase waiting time for short jobs.

### 3. RTP Pairs for Arrival Times

**Goal:**

Simulate a range of arrival patterns: front-loaded, evenly spaced, and end-loaded.

**RTP List:**

| Scenario               | Inter-Arrival RTP (Time Between Arrivals) |
| ---------------------- | ----------------------------------------- |
| Heavy front-loaded     | (0, 1)                                    |
| Medium front-loaded    | (1, 5)                                    |
| Evenly spaced arrivals | (5, 10)                                   |
| Medium end-loaded      | (10, 15)                                  |
| Heavy end-loaded       | (15, 20)                                  |

**- Explanation**:

- For `front-loaded scenarios`, many processes arrive simultaneously or within a short window.
- For `end-loaded scenarios`, arrivals are delayed, creating a “burst of activity” near the end.

### 4. RTP Pairs for Priority Distribution

**Goal:**

Simulate a spectrum from many high-priority to many low-priority processes.

**RTP List:**

| Scenario              | Priority RTP |
| --------------------- | ------------ |
| Mostly high priority  | (1, 3)       |
| Balanced distribution | (1, 10)      |
| Mostly low priority   | (8, 10)      |

**- Explanation**:

- Smaller priority values indicate higher priority (e.g., 1 is “urgent”).
- A balanced range allows all priority levels to be represented.

### 5. RTP Pairs for “Friend Values” (Aging Promotion Quantum)

**Goal:**

Explore the impact of aging parameters for promoting low-priority processes.

**RTP List:**

| Scenario               | Friend Value RTP (Aging Threshold) |
| ---------------------- | ---------------------------------- |
| Aggressive promotion   | (1, 5)                             |
| Moderate promotion     | (5, 10)                            |
| Conservative promotion | (10, 20)                           |

**- Explanation**:

- Smaller values lead to faster promotions (reduces starvation but may disrupt high-priority jobs).
- Larger values delay promotions (better for high-priority jobs but risks starvation).

### 6. Varying CPUs and IO Devices

**Goal:**

Test how performance scales with different numbers of CPUs and IO devices.

**RTP List:**

| Scenario      | Number of CPUs RTP | Number of IO Devices RTP |
| ------------- | ------------------ | ------------------------ |
| Small system  | (2, 4)             | (2, 4)                   |
| Medium system | (4, 6)             | (4, 6)                   |
| Large system  | (6, 8)             | (6, 8)                   |

**- Explanation**:

- Increasing CPUs improves throughput but introduces scheduling complexity.
- More IO devices reduce contention but require efficient IO handling.

### 7. Flip Preemption On/Off

**Goal:**

Simulate scenarios with and without preemption for fair comparison. This means you could turn On or Off preemption for ANY algorithm.

| Scenario            | Preemption |
| ------------------- | ---------- |
| Preemption enabled  | true       |
| Preemption disabled | false      |

### Summary of RTP Categories

| Category                         | Key RTP Parameters                    |
| -------------------------------- | ------------------------------------- |
| CPU vs. IO-heavy Processes       | Burst Time, IO Frequency, IO Duration |
| Round Robin Quantum              | Quantum                               |
| Arrival Times                    | Inter-Arrival Time                    |
| Priority Distribution            | Priority Levels                       |
| Aging Promotion (“Friend Value”) | Threshold for Priority Promotions     |
| CPUs and IO Devices              | Number of CPUs, Number of IO Devices  |
| Preemption Toggle                | On/Off                                |

### How to Use This in Experiments

1. Randomized Inputs:
   - Use the provided RTP ranges to generate process attributes dynamically for hundreds or thousands of runs.
   - Ensure repeatability by setting seeds for randomization.
2. Comparative Analysis:
   - Vary one parameter (e.g., time quantum) while holding others constant.
   - Observe how metrics (waiting time, turnaround time, etc.) change across scenarios.
