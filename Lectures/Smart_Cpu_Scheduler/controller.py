from scheduler import Scheduler
from Assignments.Smart_Cpu_Scheduler.hold.schedulerView import SchedulerView


class Controller:
    """Glue layer: drives scheduler ticks and view updates."""

    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.tick_timer = 0
        self.tick_interval = 1.0  # seconds per scheduler tick

    def update(self, delta_time):
        """Advance the scheduler periodically."""
        self.tick_timer += delta_time
        if self.tick_timer >= self.tick_interval:
            self.scheduler.step()
            self.tick_timer = 0
