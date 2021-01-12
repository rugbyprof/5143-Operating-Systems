"""
In this example, `worker()` tries to acquire the lock three separate times, and counts how 
many attempts it has to make to do so. In the mean time, `locker()` cycles between holding 
and releasing the lock, with short sleep in each state used to simulate load.
"""
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)
                    
def locker(lock):
    logging.debug('Locker Starting')
    while True:
        lock.acquire()
        try:
            logging.debug('Locking')
            time.sleep(1.0)
        finally:
            logging.debug('Not locking')
            lock.release()
        time.sleep(1.0)
    return
                    
def worker(lock):
    logging.debug('Worker Starting')
    num_tries = 0
    num_acquires = 0
    while num_acquires < 3:
        time.sleep(0.5)
        logging.debug('Trying to acquire')
        acquired = lock.acquire()
        try:
            num_tries += 1
            if acquired:
                logging.debug('Try #%d : Acquired',  num_tries)
                num_acquires += 1
            else:
                logging.debug('Try #%d : Not acquired', num_tries)
        finally:
            if acquired:
                lock.release()
    logging.debug('Done after %d tries', num_tries)

if __name__ == '__main__':
    lock = threading.Lock()

    locker = threading.Thread(target=locker, args=(lock,), name='Locker')
    locker.setDaemon(True)
    locker.start()

    worker1 = threading.Thread(target=worker, args=(lock,), name='Worker1')
    worker2 = threading.Thread(target=worker, args=(lock,), name='Worker2')
    worker1.start()
    worker2.start()