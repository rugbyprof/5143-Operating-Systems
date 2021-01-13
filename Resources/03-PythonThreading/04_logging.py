"""
Using the logging module to help debug your threads
"""
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                      format='[%(levelname)s] (%(threadName)-9s) %(message)s',)

def f1():
    logging.debug('Starting')
    time.sleep(1)
    logging.debug('Exiting')

def f2():
    logging.debug('Starting')
    time.sleep(2)
    logging.debug('Exiting')

def f3():
    logging.debug('Starting')
    time.sleep(3)
    logging.debug('Exiting')


t1 = threading.Thread(target=f1) # use default name
t2 = threading.Thread(name='f2', target=f2)
t3 = threading.Thread(name='f3', target=f3)

t1.start()
t2.start()
t3.start()