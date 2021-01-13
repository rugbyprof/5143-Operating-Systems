"""
By default, join() blocks indefinitely. In our sample, join() blocks 
the calling thread (main thread) until the threads (d / t) whose join() 
method is called is terminated - either normally or through an unhandled 
exception - or until the optional timeout occurs.

We can also pass a timeout argument which is a float representing the 
number of seconds to wait for the thread to become inactive. If the thread 
does not complete within the timeout period, join() returns anyway.
"""

import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

def n():
    logging.debug('Starting')
    logging.debug('Exiting')

def d():
    logging.debug('Starting')
    time.sleep(5)
    logging.debug('Exiting')

if __name__ == '__main__':

    t = threading.Thread(name='non-daemon', target=n)
    d = threading.Thread(name='daemon', target=d)
    d.setDaemon(True)

    d.start()
    t.start()

    # Try 3.0 and 7.0 to see the difference
    d.join(3.0)
    print 'd.isAlive()', d.isAlive()
    t.join()