import collections
import json


class Process:
    def __init__(self, pid, bursts, priority=0):
        self.pid = pid
        self.bursts = bursts[:]  # list of {"cpu": X} or {"io": {...}}
        self.priority = priority
        self.state = "new"
        self.remaining_time = bursts[0].get("cpu", 0) if bursts else 0

    def __repr__(self):
        return f"<P{self.pid} prio={self.priority} state={self.state} bursts={self.bursts} rem={self.remaining_time}>"


class Scheduler:
    def __init__(self, algorithm="FCFS", quantum=5):
        self.algorithm = algorithm
        self.quantum = quantum
        self.ready_queue = collections.deque()
        self.clock = 0
        self.finished = []

    def add_process(self, process):
        process.state = "ready"
        self.ready_queue.append(process)

    def run(self):
        while self.ready_queue:
            if self.algorithm == "FCFS":
                self.fcfs()
            elif self.algorithm == "RR":
                self.round_robin()
            elif self.algorithm == "SJF":
                self.sjf()
            elif self.algorithm == "PRIORITY":
                self.priority_sched()
            else:
                raise ValueError(f"Unknown algorithm: {self.algorithm}")

    # -----------------------
    # Algorithms
    # -----------------------
    def fcfs(self):
        """First Come First Serve (non-preemptive)."""
        proc = self.ready_queue.popleft()
        proc.state = "running"
        burst = proc.bursts.pop(0)
        if "cpu" in burst:
            self.clock += burst["cpu"]
        if len(proc.bursts) == 0:
            proc.state = "finished"
            self.finished.append(proc)
        else:
            proc.state = "ready"
            self.ready_queue.append(proc)

    def round_robin(self):
        """Round Robin (preemptive)."""
        proc = self.ready_queue.popleft()
        proc.state = "running"
        burst = proc.bursts[0]

        if "io" in burst:
            # If next burst is IO, just skip this process for now
            proc.state = "ready"
            proc.bursts.pop(0)
            print("io burst")
            if len(proc.bursts) == 0:
                proc.state = "finished"
                self.finished.append(proc)
                self.clock += 1  # idle tick

            return
        if "cpu" in burst:
            if burst["cpu"] > self.quantum:
                burst["cpu"] -= self.quantum
                self.clock += self.quantum
                proc.state = "ready"
                self.ready_queue.append(proc)
            else:
                self.clock += burst["cpu"]
                proc.bursts.pop(0)
                if len(proc.bursts) > 0:
                    proc.state = "ready"
                    self.ready_queue.append(proc)
                else:
                    proc.state = "finished"
                    self.finished.append(proc)
            print(len(proc.bursts))

    def round_robin_tick(self):
        if not self.ready_queue:
            self.clock += 1
            return

        proc = self.ready_queue.popleft()
        proc.state = "running"

        # print(proc)

        # Track quantum slice
        time_slice = min(self.quantum, proc.remaining_time)

        # Run tick-by-tick
        for _ in range(time_slice):
            self.clock += 1
            proc.remaining_time -= 1

            if proc.remaining_time == 0:
                proc.state = "finished"
                self.finished.append(proc)
                return  # done early

        # If not finished, requeue
        if proc.remaining_time > 0:
            proc.state = "ready"
            self.ready_queue.append(proc)

    def sjf(self):
        """
        Shortest Job First (non-preemptive).
        TODO (students):
          - Look at self.ready_queue
          - Pick the process with the *shortest next CPU burst*
          - Run it to completion (like FCFS but chosen by burst length)
        """
        # ✗ This is just a placeholder — students must implement
        raise NotImplementedError("SJF not implemented yet.")

    def priority_sched(self):
        """
        Priority Scheduling (non-preemptive).
        TODO (students):
          - Look at self.ready_queue
          - Pick the process with the *highest priority*
            (decide if low=better or high=better)
          - Run it like FCFS
        """
        # ✗ This is just a placeholder — students must implement
        raise NotImplementedError("Priority scheduling not implemented yet.")

    # -----------------------
    # Helpers
    # -----------------------
    def summary(self):
        return {
            "algorithm": self.algorithm,
            "time_elapsed": self.clock,
            "processes_finished": len(self.finished),
        }


# -------------------------------
# Example usage
# -------------------------------
if __name__ == "__main__":
    with open("generated_processes.json") as f:
        proc_defs = json.load(f)

    # Wrap JSON into Process objects (simplified: just CPU bursts for now)
    processes = [
        Process(pid=p["pid"], bursts=p["bursts"], priority=p["priority"])
        for p in proc_defs[:5]
    ]

    # Try Round Robin as a demo
    # sched = Scheduler(algorithm="RR", quantum=2)
    sched = Scheduler(algorithm="FCFS", quantum=2)
    for p in processes:
        sched.add_process(p)

    sched.run()
    print(sched.summary())

    processes = [
        Process(pid=p["pid"], bursts=p["bursts"], priority=p["priority"])
        for p in proc_defs[:5]
    ]

    sched = Scheduler(algorithm="RR", quantum=2)
    for p in processes:
        sched.add_process(p)

    sched.run()
    print(sched.summary())
