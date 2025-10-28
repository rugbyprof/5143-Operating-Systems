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
            self.current.runtime += 1  # Increment runtime
            # If the burst is done, advance to the next one (could be CPU or IO or done)
            if burst["cpu"] == 0:
                self.current.advance_burst()  # Move to the next burst
                finished_proc = self.current  # Save reference to finished process
                self.current = None  # Free the CPU
                return finished_proc  # Return the finished process
        return None

    def __repr__(self):
        return f"CPU{self.cid}: {self.current.pid if self.current else 'idle'}"
