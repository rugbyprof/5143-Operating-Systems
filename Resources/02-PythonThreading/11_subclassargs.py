"""
Because the *args and **kwargs values passed to the Thread constructor are saved 
in private variables, they are not easily accessed from a subclass. To pass arguments 
to a custom thread type, we need to redefine the constructor to save the values in 
an instance attribute that can be seen in the subclass
"""
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

class MyThread(threading.Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
		super(MyThread,self).__init__(group=group, target=target, 
			              name=name, verbose=verbose)
		self.args = args
		self.kwargs = kwargs
		return

    def run(self):
		logging.debug('running with %s and %s', self.args, self.kwargs)
		return

if __name__ == '__main__':
    for i in range(3):
	t = MyThread(args=(i,), kwargs={'a':1, 'b':2})
	t.start()