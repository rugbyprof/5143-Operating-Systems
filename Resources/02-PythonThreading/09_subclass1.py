"""
To extend the thread class you need to override the run method. 
"""
import threading
import time

class MyThread(threading.Thread):

    def run(self):
        time.sleep(5)
        return

if __name__ == '__main__':
    for i in range(3):
        t = MyThread()
        t.start()
        print 't.is_alive()=', t.is_alive()
        t.join()
        print 't.is_alive()=', t.is_alive()