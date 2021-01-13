"""
The Timer is a subclass of Thread. Timer class represents an action that should be 
run only after a certain amount of time has passed. A Timer starts its work after a 
delay, and can be canceled at any point within that delay time period.

Timers are started, as with threads, by calling their start() method. The timer can 
be stopped (before its action has begun) by calling the cancel() method. The interval 
the timer will wait before executing its action may not be exactly the same as the 
interval specified by the user.

Timer Def:
class threading.Timer(interval, function, args=None, kwargs=None)
"""

import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

def f():
    logging.debug('thread function running')
    return

if __name__ == '__main__':
    t1 = threading.Timer(5, f)
    t1.setName('t1')
    t2 = threading.Timer(5, f)
    t2.setName('t2')

    logging.debug('starting timers...')
    t1.start()
    t2.start()

    logging.debug('waiting before canceling %s', t2.getName())
    time.sleep(2)
    logging.debug('canceling %s', t2.getName())
    print 'before cancel t2.is_alive() = ', t2.is_alive()
    t2.cancel()
    # The second timer(t2) is never run because it is canceled before 
    # its wake-up.
    time.sleep(2)
    print 'after cancel t2.is_alive() = ', t2.is_alive()

    t1.join()
    t2.join()

    logging.debug('done')