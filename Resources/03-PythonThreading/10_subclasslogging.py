import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

class MyThread(threading.Thread):

    def run(self):
	logging.debug('running')
	return

if __name__ == '__main__':
    for i in range(3):
	t = MyThread()
	t.start()