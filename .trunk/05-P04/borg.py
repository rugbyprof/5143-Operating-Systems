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
