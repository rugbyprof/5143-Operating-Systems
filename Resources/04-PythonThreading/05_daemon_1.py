"""
Daemon threads run in the "background" while the main process is alive. The main
process doesn't have to keep track of the daemon or make sure its finished before 
main exits. 

Note daemon threads force main to not exit and wait for them.
"""
import threading
import time
import logging
from datetime import datetime

def logg(stuff,name=None,clear=False):
    if clear:
        with open("logfile","w") as f:
            pass
    
    with open("logfile","a") as f:
        if name:
            f.write(f'{name}')
        f.write(f'@{datetime.now()}: ')
        f.write(f'{stuff}\n')

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

def n():
    logging.debug('Starting')
    time.sleep(5) 
    logging.debug('Exiting')
    logg("n")

"""
Note that if we do not have the time.sleep(5) in the thread function d(), the daemon also exits as well:
"""

def d():
    logging.debug('Starting')
    time.sleep(4)               # comment out for different result
    logging.debug('Exiting')
    logg("d")


if __name__ == '__main__':

    t = threading.Thread(name='non-daemon', target=n)
    d = threading.Thread(name='daemon', target=d, daemon=True)
    #d.setDaemon(True)
 
    d.start()
    t.start()