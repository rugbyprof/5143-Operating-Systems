from time import sleep

from borg import Borg


class Clock(Borg):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time = kwargs.get("time", 0)
        self.sleep = kwargs.get("sleep", 0)

    def incr(self, x=1):
        if self.sleep > 0:
            sleep(self.sleep)
        self.time += x

    def __str__(self):
        return f"{self.time}"

    def __repr__(self):
        return self.__str__()


if __name__ == "__main__":
    clock = Clock(sleep=0.3)

    for i in range(15):
        clock.incr()

        print(clock)
