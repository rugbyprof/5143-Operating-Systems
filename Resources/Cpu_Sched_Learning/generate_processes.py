import json
import random
import uuid
from pathlib import Path


# ----------------------------------------------------------
# Load user class templates
# ----------------------------------------------------------
def load_user_classes(file_path="user_classes.json"):
    with open(file_path, "r") as f:
        return json.load(f)


# ----------------------------------------------------------
# Burst helpers
# ----------------------------------------------------------
def generate_cpu_burst(user_class):
    return max(
        1,
        int(random.gauss(user_class["cpu_burst_mean"], user_class["cpu_burst_stddev"])),
    )


def generate_io_burst(user_class):
    io_type = random.choice(user_class["io_profile"]["io_types"])
    duration = max(
        1,
        int(
            random.gauss(
                user_class["io_profile"]["io_duration_mean"],
                user_class["io_profile"]["io_duration_stddev"],
            )
        ),
    )
    return {"type": io_type, "duration": duration}


# ----------------------------------------------------------
# Generate one process until CPU budget is consumed
# ----------------------------------------------------------
def generate_process(user_class, max_bursts=20):
    pid = str(uuid.uuid4())[:8]

    prio_low, prio_high = user_class["priority_range"]
    priority = random.randint(prio_low, prio_high)

    # NEW: CPU time budget for this process
    budget_mean = user_class.get("cpu_budget_mean", 50)
    budget_std = user_class.get("cpu_budget_stddev", 10)
    cpu_budget = max(5, int(random.gauss(budget_mean, budget_std)))

    bursts = []
    cpu_used = 0
    burst_count = 0

    while cpu_used < cpu_budget and burst_count < max_bursts:
        # CPU burst
        cpu_burst = generate_cpu_burst(user_class)
        if cpu_used + cpu_burst > cpu_budget:
            cpu_burst = cpu_budget - cpu_used  # trim to budget
        bursts.append({"cpu": cpu_burst})
        cpu_used += cpu_burst
        burst_count += 1

        # IO burst (optional)
        if cpu_used < cpu_budget and burst_count < max_bursts:
            if random.random() < user_class["io_profile"]["io_ratio"]:
                bursts.append({"io": generate_io_burst(user_class)})
            burst_count += 1

    return {
        "pid": pid,
        "class_id": user_class["class_id"],
        "priority": priority,
        "cpu_budget": cpu_budget,
        "cpu_used": cpu_used,
        "bursts": bursts,
    }


# ----------------------------------------------------------
# Generate N processes across classes
# ----------------------------------------------------------
def generate_processes(user_classes, n=100):
    processes = []

    total_rate = sum(cls["arrival_rate"] for cls in user_classes)
    weights = [cls["arrival_rate"] / total_rate for cls in user_classes]

    for _ in range(n):
        user_class = random.choices(user_classes, weights=weights, k=1)[0]
        process = generate_process(user_class)
        processes.append(process)

    return processes


# ----------------------------------------------------------
# Example usage
# ----------------------------------------------------------
if __name__ == "__main__":
    user_classes = load_user_classes("user_classes.json")

    # Generate 10 demo processes
    processes = generate_processes(user_classes, n=10)

    # Pretty print
    for p in processes:
        print(json.dumps(p, indent=2))

    # Save to file
    out_file = Path("generated_processes.json")
    with open(out_file, "w") as f:
        json.dump(processes, f, indent=2)
    print(f"\n✅ {len(processes)} processes saved to {out_file}")
