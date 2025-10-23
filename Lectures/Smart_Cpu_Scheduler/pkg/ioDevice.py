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
