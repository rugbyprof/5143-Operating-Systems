import threading

lock = threading.Lock()

print 'First try :', lock.acquire()
print 'Second try:', lock.acquire()

print "print this if not blocked..."