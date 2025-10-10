import collections
import csv
import json
import sys


# ---------------------------------------
class Clock:
    """
    Singleton clock using Borg pattern
    All instances share the same state"""

    _shared_state = {}  # Dictionary that's shared between all instances

    def __init__(self):
        # Make the instance's __dict__ point to the shared state
        self.__dict__ = self._shared_state
        # Initialize time if not already done
        if not hasattr(self, "time"):
            self.time = 0

    def tick(self, step=1):
        """Advance the clock by 'step' units (default 1)"""
        self.time += step

    def reset(self):
        """Reset the clock to 0"""
        self.time = 0

    def now(self):
        """Get the current time"""
        return self.time


# ---------------------------------------
class Process:
    """
    Represents a process with CPU and I/O bursts
    Attributes:
        pid: unique process ID
        bursts: list of bursts [{"cpu": X}, {"io": {"type": T, "duration": D}}, ...]
        priority: scheduling priority (0 = highest)
        state: current state ("new", "ready", "running", "waiting", "finished")
    Methods:
        current_burst(): returns the current burst or None if done
        advance_burst(): moves to the next burst
        __repr__(): string representation for debugging
        __str__(): user-friendly string representation
    """

    def __init__(self, pid, bursts, priority=0):
        """Initialize process with pid, bursts, and priority"""
        self.pid = pid
        self.bursts = bursts[:]  # [{"cpu": X}, {"io": {...}}, ...]
        self.priority = priority
        self.state = "new"

    def current_burst(self):
        """Get the current burst"""
        # Return the first burst if it exists, else None
        return self.bursts[0] if self.bursts else None

    def advance_burst(self):
        """Move to the next burst"""
        if self.bursts:
            # Remove the first burst
            self.bursts.pop(0)
        # No return needed - modifies in place and current_burst() will reflect change

    def __repr__(self):
        # return self.__str__()
        return f"{self.pid}"

    def __str__(self):
        # return f"Process(pid={self.pid}, priority={self.priority}, state={self.state}, bursts={self.bursts})"
        return self.__repr__()


# ---------------------------------------
class CPU:
    """
    Represents a CPU device
    Attributes:
        cid: CPU ID
        clock: reference to the shared Clock instance
        current: currently assigned process or None
    Methods:
        is_busy(): returns True if CPU is busy
        assign(process): assigns a process to the CPU
        tick(): advances the CPU by one time unit, returns finished process if any
        __repr__(): string representation for debugging
    """

    def __init__(self, cid, clock):
        """Initialize CPU with ID and clock reference"""
        self.cid = cid
        self.clock = clock
        self.current = None

    def is_busy(self):
        """Check if the CPU is currently busy"""
        return self.current is not None

    def assign(self, process):
        """Assign a process to the CPU"""
        self.current = process
        process.state = "running"

    def tick(self):
        """
        Advance the process on the CPU by one time unit
        Returns:
             the process if it finished its CPU burst, else None
        """
        if not self.current:
            return None
        # Process the current burst
        burst = self.current.current_burst()
        # If it's a CPU burst, decrement its time
        if burst and "cpu" in burst:
            burst["cpu"] -= 1
            # If the burst is done, advance to the next one (could be CPU or IO or done)
            if burst["cpu"] == 0:
                self.current.advance_burst()  # Move to the next burst
                finished_proc = self.current  # Save reference to finished process
                self.current = None  # Free the CPU
                return finished_proc  # Return the finished process
        return None

    def __repr__(self):
        return f"CPU{self.cid}: {self.current.pid if self.current else 'idle'}"


# ---------------------------------------
class IODevice:
    """
    Represents an I/O device
    Attributes:
        did: Device ID
        dtype: Device type
        clock: reference to the shared Clock instance
        current: currently assigned process or None
    Methods:
        is_busy(): returns True if the device is busy
        assign(process): assigns a process to the device
        tick(): advances the device by one time unit, returns finished process if any
        __repr__(): string representation for debugging
    """

    def __init__(self, did, clock, dtype="GENERIC_IO"):
        """Initialize IO device with ID, type, and clock reference"""
        self.did = did
        self.dtype = dtype
        self.clock = clock
        self.current = None

    def is_busy(self):
        """Check if the IO device is currently busy"""
        return self.current is not None

    def assign(self, process):
        """Assign a process to the IO device"""
        self.current = process
        process.state = "io"  # sets the current process state to io

    def tick(self):
        """Advance the process on the IO device by one time unit"""
        if not self.current:
            return None
        # Process the current burst
        burst = self.current.current_burst()
        # If it's an I/O burst, decrement its duration
        if burst and "io" in burst:
            burst["io"]["duration"] -= 1
            # If the burst is done, advance to the next one (could be CPU or IO or done)
            if burst["io"]["duration"] == 0:
                self.current.advance_burst()  # Move to the next burst
                finished_proc = self.current  # Save reference to finished process
                self.current = None  # Free the IO device
                return finished_proc  # Return the finished process
        return None

    def __repr__(self):
        return f"IO{self.did}: {self.current.pid if self.current else 'idle'}"


# ---------------------------------------
class Scheduler:
    """
    A simple CPU and I/O scheduler

    Attributes:
        clock: shared Clock instance
        ready_queue: deque of processes ready for CPU
        wait_queue: deque of processes waiting for I/O
        cpus: list of CPU instances
        io_devices: list of IODevice instances
        finished: list of completed processes
        log: human-readable log of events
        events: structured log of events for export
        verbose: if True, print log entries to console
    Methods:
        add_process(process): add a new process to the ready queue
        step(): advance the scheduler by one time unit
        run(): run the scheduler until all processes are finished
        timeline(): return the human-readable log as a string
        export_json(filename): export the structured log to a JSON file
        export_csv(filename): export the structured log to a CSV file"""

    def __init__(self, num_cpus=1, num_ios=1, verbose=True):
        self.clock = Clock()  # shared clock instance for all components Borg pattern

        # deque (double ended queue) for efficient pops from left
        self.ready_queue = collections.deque()

        # deque (double ended queue) for efficient pops from left
        self.wait_queue = collections.deque()

        # uses a list comprehension to create a list of CPU objects
        self.cpus = [CPU(cid=i, clock=self.clock) for i in range(num_cpus)]

        # uses a list comprehension to create a list of IODevice objects
        self.io_devices = [IODevice(did=i, clock=self.clock) for i in range(num_ios)]

        self.finished = []  # list of finished processes
        self.log = []  # human-readable + snapshots
        self.events = []  # structured log for export
        self.verbose = verbose  # if True, print log entries to console

    def add_process(self, process):
        """
        Add a new process to the ready queue
        Args:
            process: Process instance to add
        Returns: None
        """

        process.state = "ready"  # sets the current process state to ready

        # adds the process to the end of the ready queue
        self.ready_queue.append(process)

        # Log the event
        self._record(
            f"{process.pid} added to ready queue",
            event_type="enqueue",
            proc=process.pid,
        )

    def _record(self, event, event_type="info", proc=None, device=None):
        """
        Record an event in the log and structured events list
        Args:
            event: description of the event
            event_type: type/category of the event (e.g., "dispatch", "enqueue", etc.)
            proc: process ID involved in the event (if any)
            device: device ID involved in the event (if any)
        Returns: None
        """
        entry = f"time={self.clock.now():<3} | {event}"
        self.log.append(entry)

        # Print to console if verbose
        if self.verbose:
            print(entry)

        # structured record for export as JSON/CSV
        self.events.append(
            {
                "time": self.clock.now(),
                "event": event,
                "event_type": event_type,
                "process": proc,
                "device": device,
                "ready_queue": [p.pid for p in self.ready_queue],
                "wait_queue": [p.pid for p in self.wait_queue],
                "cpus": [cpu.current.pid if cpu.current else None for cpu in self.cpus],
                "ios": [
                    dev.current.pid if dev.current else None for dev in self.io_devices
                ],
            }
        )

    def _snapshot(self):
        """Take a snapshot of the current state for logging"""

        # The join method is used to concatenate the process IDs in
        # the ready queue into a single string, separated by commas.
        # If the ready queue is empty, it defaults to the string "empty".
        rq = ", ".join([p.pid for p in self.ready_queue]) or "empty"

        # Same as above but for the wait queue
        wq = ", ".join([p.pid for p in self.wait_queue]) or "empty"

        # Join the status of each CPU and IO device into strings separated by " | "
        cpus = " | ".join([str(cpu) for cpu in self.cpus])

        # Same as above but for IO devices
        ios = " | ".join([str(dev) for dev in self.io_devices])

        # Creates a string snapshot of the current state of
        # the scheduler including ready queue, wait queue, CPUs, and IO devices
        snap = f"  [Ready: {rq}]  [Wait: {wq}]  Cpus:[{cpus}]  Ios:[{ios}]"

        # Append the snapshot to the log
        self.log.append(snap)
        if self.verbose:
            print(snap)

    def step(self):
        """
        Advance the scheduler by one time unit
        Returns: None
        """
        # Iterate over each CPU and tick (decrement burst time) by 1 if not idle
        for cpu in self.cpus:

            # proc is the process that just finished its CPU burst or None
            proc = cpu.tick()

            # If a process finished its CPU burst, handle it.
            # This means that proc is not None
            if proc:
                burst = proc.current_burst()

                # If the next burst is I/O, move to wait queue
                # If no more bursts, move to finished
                # If next burst is CPU, move to ready queue
                if burst and "io" in burst:
                    proc.state = "waiting"
                    self.wait_queue.append(proc)
                    self._record(
                        f"{proc.pid} finished CPU → wait queue",
                        event_type="cpu_to_io",
                        proc=proc.pid,
                        device=f"CPU{cpu.cid}",
                    )

                # If the next burst is CPU, move to ready queue
                elif burst and "cpu" in burst:
                    self.ready_queue.append(proc)

                    # logs event of moving process to ready queue
                    self._record(
                        f"{proc.pid} finished CPU → ready queue",
                        event_type="cpu_to_ready",
                        proc=proc.pid,
                        device=f"CPU{cpu.cid}",
                    )
                # No more bursts, process is finished
                else:
                    proc.state = "finished"
                    self.finished.append(proc)

                    # logs event of process finishing all bursts
                    self._record(
                        f"{proc.pid} finished all bursts",
                        event_type="finished",
                        proc=proc.pid,
                        device=f"CPU{cpu.cid}",
                    )

        # Tick IO devices
        for dev in self.io_devices:
            proc = dev.tick()
            if proc:
                burst = proc.current_burst()

                # If the next burst is I/O, move to wait queue
                # If no more bursts, move to finished
                # If next burst is CPU, move to ready queue
                if burst:
                    proc.state = "ready"
                    self.ready_queue.append(proc)

                    # logs event of moving process to ready queue
                    self._record(
                        f"{proc.pid} finished I/O → ready queue",
                        event_type="io_to_ready",
                        proc=proc.pid,
                        device=f"IO{dev.did}",
                    )
                # else process is finished
                else:
                    proc.state = "finished"
                    self.finished.append(proc)

                    # logs event of process finishing all bursts
                    self._record(
                        f"{proc.pid} finished all bursts",
                        event_type="finished",
                        proc=proc.pid,
                        device=f"IO{dev.did}",
                    )

        # Dispatch to CPUs
        for cpu in self.cpus:

            # If CPU is free and there's a process in ready queue
            if not cpu.is_busy() and self.ready_queue:

                # Pop process from left of ready queue
                proc = self.ready_queue.popleft()

                # Assign process to CPU
                cpu.assign(proc)

                # Log the dispatch event
                self._record(
                    f"{proc.pid} dispatched to CPU{cpu.cid}",
                    event_type="dispatch_cpu",
                    proc=proc.pid,
                    device=f"CPU{cpu.cid}",
                )

        # Dispatch to IO devices
        # Same logic as above but for IO devices and wait queue
        for dev in self.io_devices:
            if not dev.is_busy() and self.wait_queue:
                proc = self.wait_queue.popleft()
                dev.assign(proc)
                self._record(
                    f"{proc.pid} dispatched to IO{dev.did}",
                    event_type="dispatch_io",
                    proc=proc.pid,
                    device=f"IO{dev.did}",
                )

        if self.verbose:
            self._snapshot()
        self.clock.tick()

    def run(self):
        """
        Run the scheduler until all processes are finished
        Returns: None
        """

        # Continue stepping while there are processes in ready/wait queues
        # or any CPU/IO device is busy
        while (
            self.ready_queue
            or self.wait_queue
            or any(cpu.is_busy() for cpu in self.cpus)
            or any(dev.is_busy() for dev in self.io_devices)
        ):
            self.step()

    def timeline(self):
        """Return the human-readable log as a single string"""
        return "\n".join(self.log)

    # ---- Exporters ----
    def export_json(self, filename="timeline.json"):
        """Export the timeline to a JSON file"""
        with open(filename, "w") as f:
            json.dump(self.events, f, indent=2)
        if self.verbose:
            print(f"✅ Timeline exported to {filename}")

    def export_csv(self, filename="timeline.csv"):
        """Export the timeline to a CSV file"""

        # If there are no events, do nothing
        if not self.events:
            return

        # Write CSV using DictWriter for structured data
        # .keys() returns a list of all the keys in a dictionary.
        keys = self.events[0].keys()

        # Open the file in write mode with newline='' to prevent extra blank lines on Windows
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.events)
        if self.verbose:
            print(f"✅ Timeline exported to {filename}")


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
    sched = Scheduler(num_cpus=cpus, num_ios=ios, verbose=False)

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
