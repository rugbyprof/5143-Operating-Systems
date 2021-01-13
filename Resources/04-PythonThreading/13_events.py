"""
Event object is one of the simplest mechanisms for communication between threads: one 
thread signals an event and other threads wait for it

https://docs.python.org/3/library/threading.html.

We're using multiple threads to spin separate operations off to run concurrently, 
however, there are times when it is important to be able to synchronize two or more 
threads' operations. Using Event objects is the simple way to communicate between 
threads.

An Event manages an internal flag that callers can either set() or clear(). Other 
threads can wait() for the flag to be set(). Note that the wait() method blocks 
until the flag is true.
"""

import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)
                    
def wait_for_event(e):
    logging.debug('wait_for_event starting')
    event_is_set = e.wait()
    logging.debug('event set: %s', event_is_set)

def wait_for_event_timeout(e, t):
    while not e.isSet():
        logging.debug('wait_for_event_timeout starting')
        event_is_set = e.wait(t)
        logging.debug('event set: %s', event_is_set)
        if event_is_set:
            logging.debug('processing event')
        else:
            logging.debug('doing other things')

if __name__ == '__main__':
    e = threading.Event()
    t1 = threading.Thread(name='blocking', 
                      target=wait_for_event,
                      args=(e,))
    t1.start()

    t2 = threading.Thread(name='non-blocking', 
                      target=wait_for_event_timeout, 
                      args=(e, 2))
    t2.start()

    logging.debug('Waiting before calling Event.set()')
    time.sleep(3)
    e.set()
    logging.debug('Event is set')
    time.sleep(2)
    e.set()