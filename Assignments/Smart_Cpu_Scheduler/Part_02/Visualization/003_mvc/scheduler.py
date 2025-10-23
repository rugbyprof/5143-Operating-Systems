# =========================================================
# scheduler.py  – Pure simulation logic (no pygame)
# =========================================================
import random


class Job:
    def __init__(self, job_id, bursts):
        self.id = job_id
        self.bursts = bursts  # e.g., [5, 3, 2]
        self.current_burst = 0
        self.state = "ready"

    def __repr__(self):
        return f"P{self.id}"


class Scheduler:
    def __init__(self, jobs):
        self.clock = 0
        self.ready = jobs[:]  # initial ready queue
        self.wait = []
        self.cpu = []
        self.io = []

    # -----------------------------------------------------
    def has_jobs(self):
        """Return True if any queue still has jobs."""
        return any([self.ready, self.wait, self.cpu, self.io])

    # -----------------------------------------------------
    def step(self):
        """Advance one tick of simulation logic."""
        self.clock += 1

        # Move jobs around randomly for demo (replace with FCFS/RR/etc.)
        if self.cpu:
            job = self.cpu.pop(0)
            job.current_burst += 1
            if job.current_burst >= job.bursts[0]:
                job.state = "wait"
                job.current_burst = 0
                self.wait.append(job)
            else:
                self.cpu.append(job)
        elif self.ready:
            job = self.ready.pop(0)
            job.state = "running"
            self.cpu.append(job)

        # Random I/O completion
        if self.wait and random.random() < 0.1:
            job = self.wait.pop(0)
            job.state = "ready"
            self.ready.append(job)

    # -----------------------------------------------------
    def snapshot(self):
        """Return current state snapshot for visualization."""
        return {
            "clock": self.clock,
            "ready": [job.id for job in self.ready],
            "wait": [job.id for job in self.wait],
            "cpu": [job.id for job in self.cpu],
            "io": [job.id for job in self.io],
        }
