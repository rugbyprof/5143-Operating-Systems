"""
Basic thread example but with params being passed into function.
Threading.thread expects a tuple, and the trailing comma is intentional
"""
import threading

def f(id):
    print 'thread function %s' %(id)
    return

if __name__ == '__main__':
    for i in range(3):
        t = threading.Thread(target=f, args=(i,))
        t.start()