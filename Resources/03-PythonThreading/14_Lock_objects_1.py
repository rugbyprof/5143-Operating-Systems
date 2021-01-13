"""
 A primitive `lock` is in one of two states, "locked" or "unlocked". It is created in the unlocked state. 
 It has two basic methods, `acquire()` and `release()`. When the state is unlocked, `acquire()` changes 
 the state to locked and returns immediately. When the state is locked, `acquire()` blocks until a call 
 to `release()` in another thread changes it to unlocked, then the `acquire()` call resets it to locked 
 and returns. The `release()` method should only be called in the locked state; it changes the state to 
 unlocked and returns immediately. If an attempt is made to release an unlocked lock, a RuntimeError 
 will be raised.
"""
import threading
import time
import logging
import random

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)
                    
class Counter(object):
    def __init__(self, start = 0):
        self.lock = threading.Lock()
        self.value = start
    def increment(self):
        logging.debug('Waiting for a lock')
        self.lock.acquire()
        try:
            logging.debug('Acquired a lock')
            self.value = self.value + 1
        finally:
            logging.debug('Released a lock')
            self.lock.release()

def worker(c):
    for i in range(2):
        r = random.random()
        logging.debug('Sleeping %0.02f', r)
        time.sleep(r)
        c.increment()
    logging.debug('Done')

if __name__ == '__main__':
    counter = Counter()
    for i in range(2):
        t = threading.Thread(target=worker, args=(counter,))
        t.start()

    logging.debug('Waiting for worker threads')
    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()
    logging.debug('Counter: %d', counter.value)

