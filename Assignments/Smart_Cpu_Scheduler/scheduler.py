import collections
import csv
import json
import sys


# ---------------------------------------
# Borg Clock
# ---------------------------------------
class Clock:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        if not hasattr(self, "time"):
            self.time = 0

    def tick(self, step=1):
        self.time += step

    def reset(self):
        self.time = 0

    def now(self):
        return self.time


# ---------------------------------------
# Process
# ---------------------------------------
class Process:
    def __init__(self, pid, bursts, priority=0):
        self.pid = pid
        self.bursts = bursts[:]  # [{"cpu": X}, {"io": {...}}, ...]
        self.priority = priority
        self.state = "new"

    def current_burst(self):
        return self.bursts[0] if self.bursts else None

    def advance_burst(self):
        if self.bursts:
            self.bursts.pop(0)

    def __repr__(self):
        return f"{self.pid}"


# ---------------------------------------
# CPU class
# ---------------------------------------
class CPU:
    def __init__(self, cid, clock):
        self.cid = cid
        self.clock = clock
        self.current = None

    def is_busy(self):
        return self.current is not None

    def assign(self, process):
        self.current = process
        process.state = "running"

    def tick(self):
        if not self.current:
            return None
        burst = self.current.current_burst()
        if burst and "cpu" in burst:
            burst["cpu"] -= 1
            if burst["cpu"] == 0:
                self.current.advance_burst()
                finished_proc = self.current
                self.current = None
                return finished_proc
        return None

    def __repr__(self):
        return f"CPU{self.cid}: {self.current.pid if self.current else 'idle'}"


# ---------------------------------------
# IO Device class
# ---------------------------------------
class IODevice:
    def __init__(self, did, clock, dtype="GENERIC_IO"):
        self.did = did
        self.dtype = dtype
        self.clock = clock
        self.current = None

    def is_busy(self):
        return self.current is not None

    def assign(self, process):
        self.current = process
        process.state = "io"

    def tick(self):
        if not self.current:
            return None
        burst = self.current.current_burst()
        if burst and "io" in burst:
            burst["io"]["duration"] -= 1
            if burst["io"]["duration"] == 0:
                self.current.advance_burst()
                finished_proc = self.current
                self.current = None
                return finished_proc
        return None

    def __repr__(self):
        return f"IO{self.did}: {self.current.pid if self.current else 'idle'}"


# ---------------------------------------
# Scheduler
# ---------------------------------------
class Scheduler:
    def __init__(self, num_cpus=1, num_ios=1, verbose=True):
        self.clock = Clock()
        self.ready_queue = collections.deque()
        self.wait_queue = collections.deque()
        self.cpus = [CPU(cid=i, clock=self.clock) for i in range(num_cpus)]
        self.io_devices = [IODevice(did=i, clock=self.clock) for i in range(num_ios)]
        self.finished = []
        self.log = []  # human-readable + snapshots
        self.events = []  # structured log for export
        self.verbose = verbose

    def add_process(self, process):
        process.state = "ready"
        self.ready_queue.append(process)
        self._record(
            f"{process.pid} added to ready queue",
            event_type="enqueue",
            proc=process.pid,
        )

    def _record(self, event, event_type="info", proc=None, device=None):
        entry = f"time={self.clock.now():<3} | {event}"
        self.log.append(entry)
        if self.verbose:
            print(entry)

        # structured record
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
        rq = ", ".join([p.pid for p in self.ready_queue]) or "empty"
        wq = ", ".join([p.pid for p in self.wait_queue]) or "empty"
        cpus = " | ".join([str(cpu) for cpu in self.cpus])
        ios = " | ".join([str(dev) for dev in self.io_devices])
        snap = f"  [Ready: {rq}]  [Wait: {wq}]  [{cpus}]  [{ios}]"
        self.log.append(snap)
        if self.verbose:
            print(snap)

    def step(self):
        # Tick CPUs
        for cpu in self.cpus:
            proc = cpu.tick()
            if proc:
                burst = proc.current_burst()
                if burst and "io" in burst:
                    proc.state = "waiting"
                    self.wait_queue.append(proc)
                    self._record(
                        f"{proc.pid} finished CPU → wait queue",
                        event_type="cpu_to_io",
                        proc=proc.pid,
                        device=f"CPU{cpu.cid}",
                    )
                elif burst and "cpu" in burst:
                    self.ready_queue.append(proc)
                    self._record(
                        f"{proc.pid} finished CPU → ready queue",
                        event_type="cpu_to_ready",
                        proc=proc.pid,
                        device=f"CPU{cpu.cid}",
                    )
                else:
                    proc.state = "finished"
                    self.finished.append(proc)
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
                if burst:
                    proc.state = "ready"
                    self.ready_queue.append(proc)
                    self._record(
                        f"{proc.pid} finished I/O → ready queue",
                        event_type="io_to_ready",
                        proc=proc.pid,
                        device=f"IO{dev.did}",
                    )
                else:
                    proc.state = "finished"
                    self.finished.append(proc)
                    self._record(
                        f"{proc.pid} finished all bursts",
                        event_type="finished",
                        proc=proc.pid,
                        device=f"IO{dev.did}",
                    )

        # Dispatch to CPUs
        for cpu in self.cpus:
            if not cpu.is_busy() and self.ready_queue:
                proc = self.ready_queue.popleft()
                cpu.assign(proc)
                self._record(
                    f"{proc.pid} dispatched to CPU{cpu.cid}",
                    event_type="dispatch_cpu",
                    proc=proc.pid,
                    device=f"CPU{cpu.cid}",
                )

        # Dispatch to IO devices
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
        while (
            self.ready_queue
            or self.wait_queue
            or any(cpu.is_busy() for cpu in self.cpus)
            or any(dev.is_busy() for dev in self.io_devices)
        ):
            self.step()

    def timeline(self):
        return "\n".join(self.log)

    # ---- Exporters ----
    def export_json(self, filename="timeline.json"):
        with open(filename, "w") as f:
            json.dump(self.events, f, indent=2)
        if self.verbose:
            print(f"✅ Timeline exported to {filename}")

    def export_csv(self, filename="timeline.csv"):
        if not self.events:
            return
        keys = self.events[0].keys()
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
    with open(filename) as f:
        data = json.load(f)

    processes = []
    for p in data[:limit]:
        bursts = []
        for b in p["bursts"]:
            if "cpu" in b:
                bursts.append({"cpu": b["cpu"]})
            elif "io" in b:
                bursts.append(
                    {"io": {"type": b["io"]["type"], "duration": b["io"]["duration"]}}
                )
        proc = Process(pid=p["pid"], bursts=bursts, priority=p["priority"])
        processes.append(proc)

    return processes


def parse_value(value):
    """Try to convert string to appropriate type"""
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
    """Parse command line arguments into a dictionary"""
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
    args = argParse()
    file_num = args.get("file_num", 1)
    limit = args.get("limit", None)
    cpus = args.get("cpus", 1)
    ios = args.get("ios", 1)

    clock = Clock()
    print(f"\n=== Simulation with {cpus} CPU(s) and {ios} IO device(s) ===")
    processes = load_processes_from_json(
        f"./job_jsons/process_file_{str(file_num).zfill(4)}.json", limit=limit
    )
    sched = Scheduler(num_cpus=cpus, num_ios=ios, verbose=False)
    for p in processes:
        sched.add_process(p)

    sched.run()
    print("\n--- Final Log ---")
    print(sched.timeline())
    print(f"\nTime elapsed: {sched.clock.now()}")
    print(f"Finished: {[p.pid for p in sched.finished]}")

    # Export structured logs
    sched.export_json(f"./timelines/timeline{str(file_num).zfill(4)}.json")
    sched.export_csv(f"./timelines/timeline{str(file_num).zfill(4)}.csv")
    clock.reset()
