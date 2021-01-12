"""
All of the objects provided by a module that has acquire() and release() methods 
can be used as context managers for a with statement. The acquire() method will 
be called when the block is entered, and release() will be called when the block 
is exited (see https://docs.python.org/3/library/threading.html#with-locks)
"""
import threading
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',)

def worker_with(lock):
    with lock:
        logging.debug('Lock acquired via with')
        
def worker_not_with(lock):
    lock.acquire()
    try:
        logging.debug('Lock acquired directly')
    finally:
        lock.release()

if __name__ == '__main__':
    lock = threading.Lock()
    w = threading.Thread(target=worker_with, args=(lock,))
    nw = threading.Thread(target=worker_not_with, args=(lock,))

    w.start()
    nw.start()