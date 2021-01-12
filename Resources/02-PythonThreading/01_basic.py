"""
Basic thread example
"""
import threading

def f():
    print 'thread function'
    return

if __name__ == '__main__':
    for i in range(3):
        t = threading.Thread(target=f)
        t.start()