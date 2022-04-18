from operator import indexOf


class Borg(object):
    """A Borg class object
    This object forces all instances of it to share the same internal state.
    It is subclassable.  Each subclass only shares monostate with itself, i.e.:
    Borg classes do not share internal state with their subclasses.
    """

    __monostate = None

    def __init__(self, **kwargs):
        """Initialize a borg object
        Pass all arguments to the initialize function, if and only if the Borg
        does not already have a monostate, else, return a new Borg object with
        the current monostate.

        This version also assigns a unique id to each instance. So, even though
        they all refer to the same data, they all have a unique id. This can be
        useful in some instances.
        """
        if Borg.__monostate is not None:
            self.__dict__ = Borg.__monostate
        else:
            Borg.__monostate = self.__dict__
            self.initialize(**kwargs)

    def initialize(self, **kwargs):
        """Init function for a Borg object
        Invoked the first time a Borg object is made.  Allows setting some
        initial state of the objects.
        """
        for k, v in kwargs.items():
            self.__dict__[k] = v


class Lock(Borg):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.locked = False
        self.waitQ = []

    def __str__(self):
        s = str(id(self)) + "\n"
        for k, v in self.__dict__.items():
            s += f"{k}={v}\n"
        return s

    def acquire(self):
        if not self.locked:
            if id(self) in self.waitQ:
                self.waitQ.remove(id(self))
            self.locked = True
            return True
        return False

    def release(self):
        if self.locked:
            self.locked = False
            return True
        return False

    def wait(self):
        self.waitQ.append(id(self))


class Semaphore:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.count = kwargs.get("count", 1)
        self.acquiredList = []

    def __str__(self):
        s = str(id(self)) + "\n"
        for k, v in self.__dict__.items():
            s += f"{k}={v}\n"
        return s

    def acquire(self):
        if self.count > 0:
            self.count -= 1
            self.acquiredList.append(self.id())
            return True
        return False

    def release(self):
        if id(self) in self.acquiredList:
            self.acquiredList.remove(id(self))
            self.count -= 1
            return True
        return False


if __name__ == "__main__":
    lock1 = Lock()
    lock2 = Lock()
    lock3 = Lock()

    lock1.acquire()

    if not lock2.acquire():
        lock2.wait()

    if not lock3.acquire():
        lock3.wait()

    print(lock1)
    print(lock2)
    print(lock3)

    lock1.release()

    lock3.acquire()

    print(lock3)
    print(lock1)
    print(lock2)
