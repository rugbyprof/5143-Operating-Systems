import time, random
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

# Columns in order
STAGES = ["New", "Ready", "Running", "Exit"]

# Jobs
jobs = []
pid_counter = 1


def create_job():
    global pid_counter
    job = {
        "pid": pid_counter,
        "burst": random.randint(2, 5),  # CPU burst time
        "stage": 0,  # start at "New"
    }
    pid_counter += 1
    return job


def display():
    table = Table(title="Job Pipeline", expand=True)
    for stage in STAGES:
        table.add_column(stage, justify="center")

    # Build row: jobs get placed in their current stage
    stage_contents = [[] for _ in STAGES]
    for job in jobs:
        stage_contents[job["stage"]].append(f"PID{job['pid']}({job['burst']})")

    # Find max row length across all stages
    max_len = max(len(col) for col in stage_contents)
    for i in range(max_len):
        row = []
        for col in stage_contents:
            row.append(col[i] if i < len(col) else "")
        table.add_row(*row)

    console.clear()
    console.print(Panel(table, expand=False, title="Job Scheduling Flow"))


# Main loop
for tick in range(40):
    # Randomly add new jobs
    if random.random() < 0.3:
        jobs.append(create_job())

    # Process jobs
    for job in list(jobs):  # copy so we can modify
        if job["stage"] == 2:  # Running
            job["burst"] -= 1
            if job["burst"] <= 0:
                job["stage"] = 3  # Move to Exit
        elif job["stage"] < 2:  # New → Ready → Running
            # small chance to advance stage
            if random.random() < 0.5:
                job["stage"] += 1

    # Remove jobs in Exit after a while
    jobs = [j for j in jobs if j["stage"] < 3 or random.random() < 0.9]

    display()
    time.sleep(0.5)
