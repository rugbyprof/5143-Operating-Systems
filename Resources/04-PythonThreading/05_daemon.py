"""
Daemon threads run in the "background" while the main process is alive. The main
process doesn't have to keep track of the daemon or make sure its finished before 
main exits. 

Not daemon threads force main to not exit and wait for them.
"""
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

def n():
    logging.debug('Starting')
    time.sleep(5) 
    logging.debug('Exiting')

"""
Note that if we do not have the time.sleep(5) in the thread function d(), the daemon also exits as well:
"""

def d():
    logging.debug('Starting')
    #time.sleep(5)               # comment out for different result
    logging.debug('Exiting')



if __name__ == '__main__':

	t = threading.Thread(name='non-daemon', target=n)

	d = threading.Thread(name='daemon', target=d)
	d.setDaemon(True)

	d.start()
	t.start()