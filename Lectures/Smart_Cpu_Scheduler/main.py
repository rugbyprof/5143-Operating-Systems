"""
TODO: Add an arrival time to the generated processes and only allow entry when the clock == arrival time.
TODO: Add a quantum (time slice) countdown for Round Robin scheduling.
"""

import collections
import csv
import json
from multiprocessing import process
import sys
from rich import print

from pkg.clock import Clock
from pkg.scheduler import Scheduler
from pkg.process import Process


# ---------------------------------------
# Load JSON into Process objects
# ---------------------------------------
def load_processes_from_json(filename="generated_processes.json", limit=None):
    """Load processes from a JSON file into Process instances
    Args:
        filename: path to the JSON file
        limit: if set, only load this many processes
    Returns:
        list of Process instances
    Raises:
        FileNotFoundError if the file does not exist
    """

    # If limit is set, only load that many processes
    with open(filename) as f:
        data = json.load(f)

    processes = []

    # If limit is None or greater than available, use all
    if limit is None or limit > len(data):
        limit = len(data)

    # :limit slices the list of processes loaded from the JSON file to only include
    # the first 'limit' number of processes.
    # This is useful for testing or running simulations with a smaller subset of processes.
    for p in data[:limit]:

        # Create a list of bursts in the expected format for Process
        # [{"cpu": X}, {"io": {"type": T, "duration": D}}, ...]
        bursts = []

        # Iterate over each burst in the process's burst list
        # and append to bursts list in the correct format
        for b in p["bursts"]:
            if "cpu" in b:
                # format {"cpu": X}
                bursts.append({"cpu": b["cpu"]})

            elif "io" in b:
                # format {"io": {"type": T, "duration": D}}
                bursts.append(
                    {"io": {"type": b["io"]["type"], "duration": b["io"]["duration"]}}
                )

        proc = Process(pid=p["pid"], bursts=bursts, priority=p["priority"])
        processes.append(proc)

    return processes


def parse_value(value):
    """
    Try to convert string to appropriate type since everything read in from command line is a string
    Args:
        value: string value to parse
    Returns:
        value converted to bool, int, float, or original string
    """
    # Try boolean
    if value.lower() in ("true", "false"):
        return value.lower() == "true"
    # Try int
    try:
        return int(value)
    except ValueError:
        pass
    # Try float
    try:
        return float(value)
    except ValueError:
        pass
    # Give up, return string
    return value


def argParse():
    """Parse command line arguments into a dictionary
    Returns:
        dict of argument names to values
    """
    kwargs = {}
    for arg in sys.argv[1:]:
        if "=" in arg:
            key, value = arg.split("=", 1)
            kwargs[key] = parse_value(value)
    return kwargs


# ---------------------------------------
# Example usage
# ---------------------------------------
if __name__ == "__main__":
    # Parse command line arguments
    args = argParse()

    # Get parameters if they exist, else use defaults
    # file_num is used to load different process files and save different timeline files
    file_num = args.get("file_num", 1)

    # Limit is used to restrict the number of processes loaded
    limit = args.get("limit", None)

    # Number of CPUs and IO devices
    cpus = args.get("cpus", 1)
    ios = args.get("ios", 1)

    # Run the simulation
    clock = Clock()
    print(f"\n=== Simulation with {cpus} CPU(s) and {ios} IO device(s) ===")

    # Load processes from JSON file
    processes = load_processes_from_json(
        f"./job_jsons/process_file_{str(file_num).zfill(4)}.json", limit=limit
    )

    # Initialize scheduler and add processes
    sched = Scheduler(num_cpus=cpus, num_ios=ios, verbose=True)

    # Add processes to scheduler
    for p in processes:
        sched.add_process(p)

    # Run the scheduler
    sched.run()

    # Print final log and stats
    print("\n--- Final Log ---")
    print(sched.timeline())
    print(f"\nTime elapsed: {sched.clock.now()}")
    print(f"Finished: {[p.pid for p in sched.finished]}")

    # Export structured logs
    sched.export_json(f"./timelines/timeline{str(file_num).zfill(4)}.json")
    sched.export_csv(f"./timelines/timeline{str(file_num).zfill(4)}.csv")
    clock.reset()
