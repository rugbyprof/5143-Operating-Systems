## MLFQ Overview

For a straightforward implementation of a Multi-Level Feedback Queue (MLFQ) CPU scheduling algorithm, here’s a simple approach that incorporates these key elements:

- Setting up queues
- Determining time quantum values
- How to promote/demote between queues
- How to approach aging a job

### MLFQ Overview:

The basics:

1. A jobs starts in the highest priority queue, with the smallest time quantum.
2. If a job doesn’t finish within its time quantum, it’s moved to the next lower-priority queue with a longer time quantum.
3. Aging promotes long-waiting jobs back up to a higher-priority queue to avoid starvation.

### Queue Setup

1. Define Your Queues:
   - Each queue represents a different priority level.
   - Higher-priority queues have smaller time quantums.
2. Example of Queues:
   - Queue 1: Highest priority, smallest time quantum, say 4 ms.
   - Queue 2: Medium priority, larger time quantum, say 8 ms.
   - Queue 3: Lowest priority, longest time quantum, say 16 ms.

Jobs initially start in Queue 1. If they use up their time quantum in Queue 1 without finishing, they’re moved to Queue 2, and so on.

### Simplified Aging and Promotion

- Aging: If a job stays in a lower-priority queue for too long without execution, it’s promoted to the next higher priority queue to avoid starvation.
- Aging Threshold: You might define a threshold (e.g., 20 ms) after which a job waiting in a lower queue is promoted.

### Python Implementation Outline

Here’s a Python code outline for an MLFQ scheduler.

```python
from collections import deque

class Job:
    def __init__(self, job_id, burst_time):
        self.job_id = job_id
        self.burst_time = burst_time  # Total CPU burst time needed
        self.remaining_time = burst_time  # Time remaining for the job
        self.waiting_time = 0  # Total time spent waiting

class MLFQScheduler:
    def __init__(self):
        # Define queues with associated time quantums
        self.queues = [
            {'queue': deque(), 'quantum': 4, 'priority': 1},
            {'queue': deque(), 'quantum': 8, 'priority': 2},
            {'queue': deque(), 'quantum': 16, 'priority': 3}
        ]
        self.completed_jobs = []

    def add_job(self, job):
        # Add new jobs to the highest priority queue
        self.queues[0]['queue'].append(job)

    def schedule(self):
        # Process each queue in order
        while any(queue['queue'] for queue in self.queues):
            for level, queue_data in enumerate(self.queues):
                queue, quantum, priority = queue_data['queue'], queue_data['quantum'], queue_data['priority']

                if not queue:
                    continue

                job = queue.popleft()  # Get the next job from this queue

                # Simulate CPU time for this job based on the queue's time quantum
                execution_time = min(job.remaining_time, quantum)
                job.remaining_time -= execution_time

                # If job finishes within this quantum, it’s done
                if job.remaining_time <= 0:
                    self.completed_jobs.append(job)
                    print(f"Job {job.job_id} completed in Queue {priority}")
                else:
                    # If not finished, increase waiting time of others and demote job to next queue
                    if level + 1 < len(self.queues):
                        self.queues[level + 1]['queue'].append(job)
                        print(f"Job {job.job_id} moved to Queue {priority + 1}")
                    else:
                        # Stay in the last queue if there's no lower queue
                        queue.append(job)

                # Update waiting times for jobs in lower queues to manage aging
                for lower_queue in self.queues[level + 1:]:
                    for waiting_job in lower_queue['queue']:
                        waiting_job.waiting_time += execution_time
                        # Promote jobs that have been waiting too long
                        if waiting_job.waiting_time >= 20:  # Aging threshold
                            waiting_job.waiting_time = 0
                            lower_queue['queue'].remove(waiting_job)
                            self.queues[level]['queue'].append(waiting_job)
                            print(f"Job {waiting_job.job_id} promoted to Queue {priority}")

# Sample usage
scheduler = MLFQScheduler()
scheduler.add_job(Job(1, 10))
scheduler.add_job(Job(2, 15))
scheduler.add_job(Job(3, 25))
scheduler.schedule()
```

### Explanation

1. **Queue Setup**: The MLFQScheduler class has an array of dictionaries to represent queues, each with a time quantum and priority.
2. **Adding Jobs**: add_job() adds new jobs to the highest priority queue.
3. **Job Execution**:
   - Execution Time: Each job is executed for a duration equal to the minimum of its remaining time and the queue’s time quantum.
   - Completion: If a job’s remaining time is exhausted, it’s marked as completed.
   - Demotion: If a job doesn’t complete within its time quantum, it’s moved to the next queue.
4. **Aging**:
   - The waiting_time attribute tracks how long each job has waited.
   - If a job waits too long in a lower-priority queue (over 20 ms), it’s promoted to the next higher queue.

### Suggested Values:

- **Time Quantums**:
  - 4 ms for the highest priority
  - 8 ms for the middle priority
  - 16 ms for the lowest priority
- **Aging Threshold**: Around 20 ms works well for simple simulations.

Remember to design your code in such a manner that these values are not hard coded. You should be able to "configure" your simulation by doing something similar to:

```json
{ "TimeQuantums": [4, 6, 8, 12, 16] }
```

This implies 5 different priorities, which means 5 different queues ... (get it?)
