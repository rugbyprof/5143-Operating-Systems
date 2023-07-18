from borg import Borg
from clock import Clock
from cpu import CPU


class Scheduler(Borg):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.alg = kwargs.get("alg", "rr")
        self.quantum = kwargs.get("quantum", 5)
        self.clock = Clock()
        self.cou = CPU()
