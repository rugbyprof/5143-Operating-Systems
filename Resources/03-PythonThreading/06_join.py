"""
Docs:
join([timeout]) Wait until the thread terminates. This blocks the calling 
thread until the thread whose join() method is called terminates – either 
normally or through an unhandled exception – or until the optional timeout occurs.

Example:
If, for example, you want to concurrently download a bunch of pages to 
concatenate them into a single large page, you may start concurrent 
downloads using threads, but need to wait until the last page/thread 
is finished before you start assembling a single page out of many. That's 
when you use join().
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

	d.join()
	t.join()