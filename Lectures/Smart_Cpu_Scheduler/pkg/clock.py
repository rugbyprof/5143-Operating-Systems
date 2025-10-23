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
