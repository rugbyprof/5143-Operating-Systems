# Python Threading - Creating Threads with Python

Good Article on Threading: http://jessenoller.com/blog/2009/02/01/python-threads-and-the-global-interpreter-lock
Another good resource: https://hackernoon.com/synchronization-primitives-in-python-564f89fee732


## The threading module

Using threads allows a program to run multiple operations concurrently in the same process space. Through out this tutorials, we'll be using `threading` module. Note that there is another module called `thread` which has been renamed to `_thread` in Python 3. Actually, the `threading` module constructs higher-level threading interfaces on top of the lower level `_thread` module. We rarely touch the low level `_thread` module.


### Thread Objects

The `Thread` class is defined in http://hg.python.org/cpython/file/3.4/Lib/threading.py.

The `__init__()` of the `Thread` class looks like this:

```python
def __init__(self, group=None, target=None, name=None,
             args=(), kwargs=None, *, daemon=None):
```

In this section, we'll start with the simplest way to use a Thread. So, as shown in the code below, we instantiate it with a target function `f()` and call `start()` to let it begin working. The `target` is the callable object to be invoked by the `run()` method. Defaults to `None`, meaning nothing is called.

```python
import threading

def f():
    print 'thread function'
    return

if __name__ == '__main__':
    for i in range(3):
        t = threading.Thread(target=f)
        t.start()
```

The `start()` starts the thread's activity. It must be called at most once per thread object. It arranges for the object's `run()` method to be invoked in a separate thread of control.

This method will raise a RuntimeError if called more than once on the same thread object.

The code will output "thread function" three times:

```
thread function
thread function
thread function
```

 

### start() & run() methods

The `run()` method is called by `start()` method (check [threading.py](http://hg.python.org/cpython/file/3.4/Lib/threading.py)):

```python
class Thread:
    ...

    def start(self):
        """Start the thread's activity.

        It must be called at most once per thread object. It arranges for the
        object's run() method to be invoked in a separate thread of control.

        This method will raise a RuntimeError if called more than once on the
        same thread object.

        """
        if not self._initialized:
            raise RuntimeError("thread.__init__() not called")

        if self._started.is_set():
            raise RuntimeError("threads can only be started once")
        with _active_limbo_lock:
            _limbo[self] = self
        try:
            _start_new_thread(self._bootstrap, ())
        except Exception:
            with _active_limbo_lock:
                del _limbo[self]
            raise
        self._started.wait()

    def _bootstrap(self):
        try:
            self._bootstrap_inner()
        except:
            if self._daemonic and _sys is None:
                return
            raise

    def _bootstrap_inner(self):
        try:
         ...

            try:
                self.run()
            except SystemExit:
                pass
            except:
```



### Passing parameters
To make a thread more useful, we want to pass `args` to give more information about the work. The code below passes an integer for thread id, and then the thread prints it. The `args` is the argument tuple for the target invocation. Defaults to ().

```python
import threading

def f(id):
    print 'thread function %s' %(id)
    return

if __name__ == '__main__':
    for i in range(3):
        t = threading.Thread(target=f, args=(i,))
        t.start()
```

New output:

```
thread function 0
thread function 1
thread function 2
```

Now the integer argument is included in the message printed by each thread.

--------------------------------------------------------

# Identifying threads - naming and logging

## Identifying threads

While each Thread instance has a name with a default value that can be changed as the thread is created. Naming threads is useful in server processes with multiple service threads handling different operations.

```python
import threading
import time

def f1():
    print threading.currentThread().getName(), 'Starting'
    time.sleep(1)
    print threading.currentThread().getName(), 'Exiting'

def f2():
    print threading.currentThread().getName(), 'Starting'
    time.sleep(2)
    print threading.currentThread().getName(), 'Exiting'

def f3():
    print threading.currentThread().getName(), 'Starting'
    time.sleep(3)
    print threading.currentThread().getName(), 'Exiting'

t1 = threading.Thread(target=f1) # use default name
t2 = threading.Thread(name='f2', target=f2)
t3 = threading.Thread(name='f3', target=f3)

t1.start()
t2.start()
t3.start()
```

Output:

```
Thread-1 Starting
f2 Starting
f3 Starting
Thread-1 Exiting
f2 Exiting
f3 Exiting
```
Now the `t2` and `t3` threads have their names while `t1` has a default name. 



### logging module
We were able to identify which thread is which by printing out the names of the threads, however, what we really need is the support from a logging module which will embed the thread name in every log message using the formatter code `%(threadName)s`. Including thread names in log messages makes it easier to trace those messages back to their source. Note that logging is thread-safe, so messages from different threads are kept distinct in the output.

```python
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
```

Output:

```
[DEBUG] (Thread-1 ) Starting
[DEBUG] (f2       ) Starting
[DEBUG] (f3       ) Starting
[DEBUG] (Thread-1 ) Exiting
[DEBUG] (f2       ) Exiting
[DEBUG] (f3       ) Exiting
```

The following keyword arguments are supported (from [here](https://docs.python.org/2/library/logging.html)):

| Format	| Description |
|:--------:|-------------|
| filename	| Specifies that a FileHandler be created, using the specified filename, rather than a StreamHandler. |
| filemode	| Specifies the mode to open the file, if filename is specified (if filemode is unspecified, it defaults to 'a'). |
| format	| Use the specified format string for the handler. |
| datefmt	| Use the specified date/time format. |
| level	Set | the root logger level to the specified level. |
| stream	| Use the specified stream to initialize the StreamHandler. Note that this argument is incompatible with 'filename' - if both are present, 'stream' is ignored. |

--------------------------------------------------------

# Daemon thread & join() method

## daemon threads

Daemons are only useful when the main program is running, and it's okay to kill them off once the other non-daemon threads have exited. Without daemon threads, we have to keep track of them, and tell them to exit, before our program can completely quit. By setting them as daemon threads, we can let them run and forget about them, and when our program quits, any daemon threads are killed automatically.

Usually our main program implicitly waits until all other threads have completed their work. However, sometimes programs spawn a thread as a daemon that runs without blocking the main program from exiting. Using daemon threads is useful for services where there may not be an easy way to interrupt the thread or where letting the thread die in the middle of its work without losing or corrupting data. To designate a thread as a daemon, we call its setDaemon() method with a boolean argument. The default setting for a thread is non-daemon. So, passing True turns the daemon mode on.

```python
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
```

Output:

```
(daemon   ) Starting
(non-daemon) Starting
(non-daemon) Exiting
```

As we can see from the output, it does not have "Exiting" message from the daemon thread, since all of the non-daemon threads (including the main thread) exit before the daemon thread wakes up from its five second sleep.

Note that if we do not have the `time.sleep(5)` in the thread function `d()`, the daemon also exits as well:

```
(daemon   ) Starting
(daemon   ) Exiting
(non-daemon) Starting
(non-daemon) Exiting
```
 

### join()
To wait until a daemon thread has completed its work, we may want to use `join()` method.

```python
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
```

Output:

```
(daemon   ) Starting
(non-daemon) Starting
(non-daemon) Exiting
(daemon   ) Exiting
```

We can see the exit of daemon thread about 5 seconds after the exit of the non-daemon.

By default, join() blocks indefinitely. In our sample, `join()` blocks the calling thread (main thread) until the threads (d / t) whose join() method is called is terminated - either normally or through an unhandled exception - or until the optional timeout occurs.

We can also pass a ***timeout argument*** which is a float representing the number of seconds to wait for the thread to become inactive. If the thread does not complete within the timeout period, join() returns anyway.

When the timeout argument is present and not `None`, it should be a floating point number specifying a timeout for the operation in seconds (or fractions thereof). As `join()` always returns None, we must call `isAlive()` after join() to decide whether a timeout happened - if the thread is still alive, the join() call timed out.

The following code is using timeout argument (3 seconds) which is shorter than the sleep (5 seconds).

```python
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

    d.join(3.0)
    print 'd.isAlive()', d.isAlive()
    t.join()
```

Output:

```
(daemon   ) Starting
(non-daemon) Starting
(non-daemon) Exiting
d.isAlive() True
```

After 3 seconds, the join was timed out, and the daemon thread is still alive and sleep. The `main` thread and t exited before the daemon thread wakes up from its five second sleep.

In other words, since the timeout passed is less than the amount of time the daemon thread sleeps, the thread is still "alive" after `join()` returns.

However, if we set the timeout 7 seconds:

```
d.join(7.0)
```

the daemon wakes up during the period and exits, and we will have the following output:

```
(daemon   ) Starting
(non-daemon) Starting
(non-daemon) Exiting
(daemon   ) Exiting
d.isAlive() False
```

--------------------------------------------------------

# Active threads & enumerate() method

### threading.enumerate()

It is not necessary to retain an explicit handle to all of the daemon threads in order to ensure they have completed before exiting the main process.

`threading.enumerate()` returns a list of all Thread objects currently alive. The list includes daemonic threads, dummy thread objects created by `current_thread()`, and the main thread. It excludes terminated threads and threads that have not yet been started.

```python
import threading
import time
import logging
import random

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

def f():
    t = threading.currentThread()
    r = random.randint(1,10)
    logging.debug('sleeping %s', r)
    time.sleep(r)
    logging.debug('ending')
    return

if __name__ == '__main__':
    for i in range(3):
        t = threading.Thread(target=f)
        t.setDaemon(True)
        t.start()

    main_thread = threading.current_thread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        logging.debug('joining %s', t.getName())
        t.join()
```


After `threading.enumerate()` gathers all active threads including the calling thread (main_thread), the code calls join() methods of those threads except the `main_thread`.

Output:

```
(daemon   ) Starting
(non-daemon) Starting
(non-daemon) Exiting
Output looks like this:
```

```
(Thread-1 ) sleeping 6
(Thread-2 ) sleeping 10
(MainThread) joining Thread-1
(Thread-3 ) sleeping 5
(Thread-3 ) ending
(Thread-1 ) ending
(MainThread) joining Thread-2
(Thread-2 ) ending
(MainThread) joining Thread-3
```

--------------------------------------------------------

# Subclassing & overriding run() and __init__() methods

### run() methods

So far, we've been using a thread by instantiating the `Thread` class given by the package ([threading.py](http://hg.python.org/cpython/file/3.4/Lib/threading.py_). To create our own thread in Python, we'll want to make our class to work as a thread. For this, we should subclass our class from the Thread class.

First thing we need to do is to import Thread using the following code:

```python
from threading import Thread
```

Then, we should subclass our class from the Thread class like this:

```python
class MyThread(Thread):
```

Just for reference, here is a code snippet from the package for the Thread class:

```python
class Thread:
    ...

    def start(self):
        """Start the thread's activity.

        It must be called at most once per thread object. It arranges for the
        object's run() method to be invoked in a separate thread of control.

        This method will raise a RuntimeError if called more than once on the
        same thread object.

        """
        if not self._initialized:
            raise RuntimeError("thread.__init__() not called")

        if self._started.is_set():
            raise RuntimeError("threads can only be started once")
        with _active_limbo_lock:
            _limbo[self] = self
        try:
            _start_new_thread(self._bootstrap, ())
        except Exception:
            with _active_limbo_lock:
                del _limbo[self]
            raise
        self._started.wait()

    def _bootstrap(self):
        try:
            self._bootstrap_inner()
        except:
            if self._daemonic and _sys is None:
                return
            raise

    def _bootstrap_inner(self):
        try:
         ...

            try:
                self.run()
            except SystemExit:
                pass
            except:

    def run(self):
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs
```

As a Thread starts up, it does some basic initialization and then calls its run() method, which calls the target function passed to the constructor. The Thread class represents an activity that runs in a separate thread of control. There are two ways to specify the activity:

- by passing a callable object to the constructor
- by overriding the run() method in a subclass

No other methods (except for the constructor) should be overridden in a subclass. In other words, we only override the `__init__()` and `run()` methods of a class.


In this section, we will create a subclass of Thread and override `run()` to do whatever is necessary:

```python
import threading

class MyThread(threading.Thread):

    def run(self):
        pass

if __name__ == '__main__':
    for i in range(3):
        t = MyThread()
        t.start()
```

Once a thread object is created, its activity must be started by calling the thread's `start()` method. This invokes the `run()` method in a separate thread of control.

Once the thread's activity is started, the thread is considered 'alive'. It stops being alive when its run() method terminates - either normally, or by raising an unhandled exception. The `is_alive()` method tests whether the thread is alive.

```python
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
```

Output:

```
t.is_alive()= True
t.is_alive()= False
t.is_alive()= True
t.is_alive()= False
t.is_alive()= True
t.is_alive()= False
```

As we can see from the output, each of the three thread is alive just after the start but `t.is_alive()=False` after terminated.

Before we move forward, for our convenience, let's put a logging feature into a place:

```python
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
```

Output:

```
(Thread-1 ) running
(Thread-2 ) running
(Thread-3 ) running
```


### Passing args to the customized thread

Because the `*args` and `**kwargs` values passed to the Thread constructor are saved in private variables, they are not easily accessed from a subclass. To pass arguments to a custom thread type, we need to redefine the constructor to save the values in an instance attribute that can be seen in the subclass:

```python
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

class MyThread(threading.Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
	super(MyThread,self).__init__(group=group, target=target, 
			              name=name, verbose=verbose)
	self.args = args
	self.kwargs = kwargs
	return

    def run(self):
	logging.debug('running with %s and %s', self.args, self.kwargs)
	return

if __name__ == '__main__':
    for i in range(3):
	t = MyThread(args=(i,), kwargs={'a':1, 'b':2})
	t.start()
```

Output:

```
(Thread-1 ) running with (0,) and {'a': 1, 'b': 2}
(Thread-2 ) running with (1,) and {'a': 1, 'b': 2}
(Thread-3 ) running with (2,) and {'a': 1, 'b': 2}
```

We overrided the `__init__()` using:

```python
super(MyThread,self).__init__()
```

For Python 3, we could have used without any args within the `super()`, like this:

```python
super().__init__()
```

--------------------------------------------------------

# Timer Object

The `Timer` is a subclass of `Thread`. `Timer` class represents an action that should be run only after a certain amount of time has passed. A Timer starts its work after a delay, and can be canceled at any point within that delay time period.

Timers are started, as with threads, by calling their `start()` method. The timer can be stopped (before its action has begun) by calling the `cancel()` method. The interval the timer will wait before executing its action may not be exactly the same as the interval specified by the user.

```python
import threading
import time

def hello():
    print("hello, Timer")

if __name__ == '__main__':
    t = threading.Timer(3.0, hello)
    t.start()
```

After 3 seconds, "hello, Timer" will be printed.

The definition for the `Timer` looks like this:

```python
class threading.Timer(interval, function, args=None, kwargs=None)
```

### Timer with threads

```python
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

def f():
    logging.debug('thread function running')
    return

if __name__ == '__main__':
    t1 = threading.Timer(5, f)
    t1.setName('t1')
    t2 = threading.Timer(5, f)
    t2.setName('t2')

    logging.debug('starting timers...')
    t1.start()
    t2.start()

    logging.debug('waiting before canceling %s', t2.getName())
    time.sleep(2)
    logging.debug('canceling %s', t2.getName())
    print 'before cancel t2.is_alive() = ', t2.is_alive()
    t2.cancel()
    time.sleep(2)
    print 'after cancel t2.is_alive() = ', t2.is_alive()

    t1.join()
    t2.join()

    logging.debug('done')
```

Output:

```
(MainThread) starting timers...
(MainThread) waiting before canceling t2
(MainThread) canceling t2
before cancel t2.is_alive() =  True
after cancel t2.is_alive() =  False
(t1       ) thread function running
(MainThread) done
```

Notice that the second `timer(t2)` is never run because it is canceled before its wake-up.



--------------------------------------------------------
# Event objects - set() & wait() methods

## Event Objects

Event object is one of the simplest mechanisms for communication between threads: one thread signals an event and other threads wait for it 
- https://docs.python.org/3/library/threading.html.

We're using multiple threads to spin separate operations off to run concurrently, however, there are times when it is important to be able to synchronize two or more threads' operations. Using `Event` objects is the simple way to communicate between threads.

An Event manages an internal flag that callers can either `set()` or `clear()`. Other threads can `wait()` for the flag to be set(). Note that the `wait()` method blocks until the flag is true.

```python
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)
                    
def wait_for_event(e):
    logging.debug('wait_for_event starting')
    event_is_set = e.wait()
    logging.debug('event set: %s', event_is_set)

def wait_for_event_timeout(e, t):
    while not e.isSet():
        logging.debug('wait_for_event_timeout starting')
        event_is_set = e.wait(t)
        logging.debug('event set: %s', event_is_set)
        if event_is_set:
            logging.debug('processing event')
        else:
            logging.debug('doing other things')

if __name__ == '__main__':
    e = threading.Event()
    t1 = threading.Thread(name='blocking', 
                      target=wait_for_event,
                      args=(e,))
    t1.start()

    t2 = threading.Thread(name='non-blocking', 
                      target=wait_for_event_timeout, 
                      args=(e, 2))
    t2.start()

    logging.debug('Waiting before calling Event.set()')
    time.sleep(3)
    e.set()
    logging.debug('Event is set')
```

The `wait()` method takes an argument representing the number of seconds to wait for the event before timing out. It returns a boolean indicating whether or not the event is set, so the caller knows why `wait()` returned. The `isSet()` method can be used separately on the event, and it's a non-blocking call.


Output:

```
(blocking ) wait_for_event starting
(MainThread) Waiting before calling Event.set()
(non-blocking) wait_for_event_timeout starting
(non-blocking) event set: False
(non-blocking) doing other things
(non-blocking) wait_for_event_timeout starting
(MainThread) Event is set
(blocking ) event set: True
(non-blocking) event set: True
(non-blocking) processing event
```

The `wait(timeout=None)` blocks until the internal flag is true by the `set()` method. If the internal flag is true on entry, return immediately. In the example, we're not setting it on entry but we're doing it much later.

If not set, the `wait()` blocks until

- another thread calls set() to set the flag to true
- or until the optional timeout occurs.

When the timeout argument is present and not `None`, it should be a floating point number specifying a timeout for the operation in seconds (or fractions thereof).

`wait()` returns true if and only if the internal flag has been set to true, either before the wait call or after the wait starts, so it will always return True except if a timeout is given and the operation times out.

In our example, `wait_for_event_timeout()` checks the event status without blocking indefinitely since timeout is given, `e.wait(t)`. However, the `wait_for_event()` blocks on the call to `wait()` does not return until the event status changes.



--------------------------------------------------------

# Lock objects - acquire() & release() methods

## Lock Objects

In this chapter, we'll learn how to control access to shared resources. The control is necessary to prevent corruption of data. In other words, to guard against simultaneous access to an object, we need to use a `Lock object`.

A primitive `lock` is a synchronization primitive that is not owned by a particular thread when locked. In Python, it is currently the lowest level synchronization primitive available, implemented directly by the `_thread` extension module.
- https://docs.python.org/3/library/threading.html.

A primitive `lock` is in one of two states, "locked" or "unlocked". It is created in the unlocked state. It has two basic methods, `acquire()` and `release()`. When the state is unlocked, `acquire()` changes the state to locked and returns immediately. When the state is locked, `acquire()` blocks until a call to `release()` in another thread changes it to unlocked, then the `acquire()` call resets it to locked and returns. The `release()` method should only be called in the locked state; it changes the state to unlocked and returns immediately. If an attempt is made to release an unlocked lock, a RuntimeError will be raised.

Here is our example code using the Lock object. In the code the `worker()` function increments a `Counter` instance, which manages a Lock to prevent two threads from changing its internal state at the same time.

```python
import threading
import time
import logging
import random

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)
                    
class Counter(object):
    def __init__(self, start = 0):
        self.lock = threading.Lock()
        self.value = start
    def increment(self):
        logging.debug('Waiting for a lock')
        self.lock.acquire()
        try:
            logging.debug('Acquired a lock')
            self.value = self.value + 1
        finally:
            logging.debug('Released a lock')
            self.lock.release()

def worker(c):
    for i in range(2):
        r = random.random()
        logging.debug('Sleeping %0.02f', r)
        time.sleep(r)
        c.increment()
    logging.debug('Done')

if __name__ == '__main__':
    counter = Counter()
    for i in range(2):
        t = threading.Thread(target=worker, args=(counter,))
        t.start()

    logging.debug('Waiting for worker threads')
    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()
    logging.debug('Counter: %d', counter.value)
```

Output:

```
(Thread-1 ) Sleeping 0.04
(MainThread) Waiting for worker threads
(Thread-2 ) Sleeping 0.11
(Thread-1 ) Waiting for a lock
(Thread-1 ) Acquired a lock
(Thread-1 ) Released a lock
(Thread-1 ) Sleeping 0.30
(Thread-2 ) Waiting for a lock
(Thread-2 ) Acquired a lock
(Thread-2 ) Released a lock
(Thread-2 ) Sleeping 0.27
(Thread-1 ) Waiting for a lock
(Thread-1 ) Acquired a lock
(Thread-1 ) Released a lock
(Thread-1 ) Done
(Thread-2 ) Waiting for a lock
(Thread-2 ) Acquired a lock
(Thread-2 ) Released a lock
(Thread-2 ) Done
(MainThread) Counter: 4
```

Another example

In this example, `worker()` tries to acquire the lock three separate times, and counts how many attempts it has to make to do so. In the mean time, `locker()` cycles between holding and releasing the lock, with short sleep in each state used to simulate load.

```python
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)
                    
def locker(lock):
    logging.debug('Starting')
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
    logging.debug('Starting')
    num_tries = 0
    num_acquires = 0
    while num_acquires < 3:
        time.sleep(0.5)
        logging.debug('Trying to acquire')
        acquired = lock.acquire(0)
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

    worker = threading.Thread(target=worker, args=(lock,), name='Worker')
    worker.start()
```

Output:

```
(Locker   ) Starting
(Locker   ) Locking
(Worker   ) Starting
(Worker   ) Trying to acquire
(Worker   ) Try #1 : Not acquired
(Locker   ) Not locking
(Worker   ) Trying to acquire
(Worker   ) Try #2 : Acquired
(Worker   ) Trying to acquire
(Worker   ) Try #3 : Acquired
(Locker   ) Locking
(Worker   ) Trying to acquire
(Worker   ) Try #4 : Not acquired
(Worker   ) Trying to acquire
(Worker   ) Try #5 : Not acquired
(Locker   ) Not locking
(Worker   ) Trying to acquire
(Worker   ) Try #6 : Acquired
(Worker   ) Done after 6 tries
```


--------------------------------------------------------

# RLock (Reentrant) objects - acquire() method

## Re-entrancy

A code is re-entrant if it can be safely called again. In other words, re-entrant code can be called more than once, even though called by different threads, it still works correctly. So, the re-entrant section of code usually use local variables only in such a way that each and every call to the code gets its own unique copy of data.

Re-entrant methods are more constrained than thread-safe methods. This is because it is safe to call re-entrant methods simultaneously from multiple threads only if each invocation results only in unique data being accessed, such as local variables.

- Non-entrant code:

```python
g = 1

def f1():
  g = g + 2;
  return g;

def f2():
  return f1() + 2;
```

If two concurrent threads access g_var, the result depends on the time of execution of each thread.

- Re-entrant code:

```python
def f(i): 
   return i + 2 

def h(i): 
   return f(i) + 2; 
```


### RLock Objects

Normal Lock objects cannot be acquired more than once, even by the same thread. This can introduce undesirable side-effects if a lock is accessed by more than one function in the same call chain:

```python
import threading

lock = threading.Lock()

print 'First try :', lock.acquire()
print 'Second try:', lock.acquire(0)
print "print this if not blocked..."
```

Output:

```
First try : True
Second try: False
print this if not blocked...
```

As we can see from the code, since both functions are using the same global lock, and one calls the other, the second acquisition fails and would have blocked using the default arguments to `acquire(blocking=True, timeout=-1)` as shown in the following code and output:

```python
import threading

lock = threading.Lock()

print 'First try :', lock.acquire()
print 'Second try:', lock.acquire()

print "print this if not blocked..."
```

This code is blocking:

```
First try : True
Second try:
```

So, as in the example above, in a situation where separate code from the same thread needs to "re-acquire" the lock, we need to use an `threading.RLock` instead of a simple `threading.Lock()`:

```python
import threading

lock = threading.RLock()

print 'First try :', lock.acquire()
print 'Second try:', lock.acquire(0)
```

Output shows that we're able to "re-acquire" the lock:

```
First try : True
Second try: 1
```

### Example Usage:

```python
class X:
    def __init__(self):
        self.a = 1
        self.b = 2
        self.lock = threading.RLock()

    def changeA(self):
        with self.lock:
            self.a = self.a + 1

    def changeB(self):
        with self.lock:
            self.b = self.b + self.a

    def changeAandB(self):
        # you can use chanceA and changeB threadsave!
        with self.lock:
            self.changeA() # a usual lock would block in here
            self.changeB()
```

--------------------------------------------------------

# Multithreading : Using locks in the with statement (Context Manager)

## Using locks in the with statement

All of the objects provided by a module that has acquire() and release() methods can be used as `context managers` for a `with` statement. The `acquire()` method will be called when the block is entered, and release() will be called when the block is exited 
(see https://docs.python.org/3/library/threading.html#with-locks)

```python
with some_lock:
    # do something...
```

is equivalent to:

```python
some_lock.acquire()
try:
    # do something...
finally:
    some_lock.release()
```


Locks implement the context manager API and are compatible with the with statement. By using locks in the with statement, we do not need to explicitly acquire and release the lock:

```python
import threading
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',)

def worker_with(lock):
    with lock:
        logging.debug('Lock acquired via with')
        
def worker_not_with(lock):
    lock.acquire()
    try:
        logging.debug('Lock acquired directly')
    finally:
        lock.release()

if __name__ == '__main__':
    lock = threading.Lock()
    w = threading.Thread(target=worker_with, args=(lock,))
    nw = threading.Thread(target=worker_not_with, args=(lock,))

    w.start()
    nw.start()
```

Output:

```
(Thread-1 ) Lock acquired via with
(Thread-2 ) Lock acquired directly
```


--------------------------------------------------------

# Condition objects with producer and consumer

## Condition objects

In this chapter, we'll learn another way of synchronizing threads: using a `Condition` object. Because a condition variable is always associated with some kind of lock, it can be tied to a shared resource. A lock can be passed in or one will be created by default. Passing one in is useful when several condition variables must share the same lock. The lock is part of the condition object: we don't have to track it separately. So, the condition object allows threads to wait for the resource to be updated.

In the following example, the consumer threads wait for the Condition to be set before continuing. The producer thread is responsible for setting the condition and notifying the other threads that they can continue.

```python
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

def consumer(cv):
    logging.debug('Consumer thread started ...')
    with cv:
    	logging.debug('Consumer waiting ...')
        cv.wait()
        logging.debug('Consumer consumed the resource')

def producer(cv):
    logging.debug('Producer thread started ...')
    with cv:
        logging.debug('Making resource available')
        logging.debug('Notifying to all consumers')
        cv.notifyAll()

if __name__ == '__main__':
    condition = threading.Condition()
    cs1 = threading.Thread(name='consumer1', target=consumer, args=(condition,))
    cs2 = threading.Thread(name='consumer2', target=consumer, args=(condition,))
    pd = threading.Thread(name='producer', target=producer, args=(condition,))

    cs1.start()
    time.sleep(2)
    cs2.start()
    time.sleep(2)
    pd.start()
```


Output:

```
(consumer1) Consumer thread started ...
(consumer1) Consumer waiting ...
(consumer2) Consumer thread started ...
(consumer2) Consumer waiting ...
(producer ) Producer thread started ...
(producer ) Making resource available
(producer ) Notifying to all consumers
(consumer1) Consumer consumed the resource
(consumer2) Consumer consumed the resource
```

Note that we did not use `acquire()` and `release()` methods at all since we utilized the lock object's context manager function (Using locks in the with statement - context manager). Instead, our threads used with to acquire the lock associated with the `Condition`.

The `wait()` method releases the lock, and then blocks until another thread awakens it by calling `notify()` or `notify_all()`.

Note that the `notify()` and `notify_all()` methods don't release the lock; this means that the thread or threads awakened will not return from their wait() call immediately, but only when the thread that called `notify()` or `notify_all()` finally relinquishes ownership of the lock.

The typical programming style using condition variables uses the lock to synchronize access to some shared state; threads that are interested in a particular change of state call wait() repeatedly until they see the desired state, while threads that modify the state call `notify()` or `notify_all()` when they change the state in such a way that it could possibly be a desired state for one of the waiters.

For example, the following code is a generic producer-consumer situation with unlimited buffer capacity:

```python
# Consume one item
with cv:
    while not an_item_is_available():
        cv.wait()
    get_an_available_item()

# Produce one item
with cv:
    make_an_item_available()
    cv.notify()
```


--------------------------------------------------------

# Producer and Consumer with Queue

## Queue

In this chapter, we'll implement another version of Producer and Consumer code with `Queue` (see Condition objects with producer and consumer).

In the following example, the Consumer and Producer threads runs indefinitely while checking the status of the queue. The Producer thread is responsible for putting items into the queue if it is not full while the Consumer thread consumes items if there are any.

```python
import threading
import time
import logging
import random
import Queue

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

BUF_SIZE = 10
q = Queue.Queue(BUF_SIZE)

class ProducerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ProducerThread,self).__init__()
        self.target = target
        self.name = name

    def run(self):
        while True:
            if not q.full():
                item = random.randint(1,10)
                q.put(item)
                logging.debug('Putting ' + str(item)  
                              + ' : ' + str(q.qsize()) + ' items in queue')
                time.sleep(random.random())
        return

class ConsumerThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(ConsumerThread,self).__init__()
        self.target = target
        self.name = name
        return

    def run(self):
        while True:
            if not q.empty():
                item = q.get()
                logging.debug('Getting ' + str(item) 
                              + ' : ' + str(q.qsize()) + ' items in queue')
                time.sleep(random.random())
        return

if __name__ == '__main__':
    
    p = ProducerThread(name='producer')
    c = ConsumerThread(name='consumer')

    p.start()
    time.sleep(2)
    c.start()
    time.sleep(2)
```



Output:

```
(producer ) Putting 2 : 1 items in queue
(producer ) Putting 10 : 2 items in queue
(producer ) Putting 6 : 3 items in queue
(producer ) Putting 7 : 4 items in queue
(producer ) Putting 1 : 5 items in queue
(consumer ) Getting 2 : 4 items in queue
(consumer ) Getting 10 : 3 items in queue
(producer ) Putting 1 : 4 items in queue
(producer ) Putting 8 : 5 items in queue
(consumer ) Getting 6 : 4 items in queue
(producer ) Putting 10 : 5 items in queue
...
```

- Since the Queue has a Condition and that condition has its Lock we don't need to bother about Condition and Lock.

>Producer uses `Queue.put(item[, block[, timeout]])` to insert data in the queue. It has the logic to acquire the lock before inserting data in queue. If optional args `block` is true and `timeout` is `None` (the default), block if necessary until a free slot is available. If timeout is a positive number, it blocks at most timeout seconds and raises the Full exception if no free slot was available within that time. Otherwise (block is false), put an item on the queue if a free slot is immediately available, else raise the Full exception (timeout is ignored in that case).

- Also put() checks whether the queue is full, then it calls wait() internally and so producer starts waiting.
- Consumer uses `Queue.get([block[, timeout]])`, and it acquires the lock before removing data from queue. If the queue is empty, it puts consumer in waiting state.
- `Queue.get()` and `Queue.get()` has `notify()` method.




--------------------------------------------------------

# Semaphore objects & Thread Pool

## Semaphore objects

This is one of the oldest synchronization primitives in the history of computer science, invented by the early Dutch computer scientist Edsger W. Dijkstra (he used the names `P()` and `V()` instead of `acquire()` and `release()`)
- from https://docs.python.org/3/library/threading.html

A semaphore manages an internal counter which is decremented by each `acquire()` call and incremented by each `release()` call. The counter can never go below zero; when `acquire()` finds that it is zero, it blocks, waiting until some other thread calls `release()`.

There are many cases we may want to allow more than one worker access to a resource while still limiting the overall number of accesses.

For example, we may want to use `semaphore` in a situation where we need to support concurrent connections/downloads. Semaphores are also often used to guard resources with limited capacity, for example, a database server.

```python
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

class ThreadPool(object):
    def __init__(self):
        super(ThreadPool, self).__init__()
        self.active = []
        self.lock = threading.Lock()
    def makeActive(self, name):
        with self.lock:
            self.active.append(name)
            logging.debug('Running: %s', self.active)
    def makeInactive(self, name):
        with self.lock:
            self.active.remove(name)
            logging.debug('Running: %s', self.active)

def f(s, pool):
    logging.debug('Waiting to join the pool')
    with s:
        name = threading.currentThread().getName()
        pool.makeActive(name)
        time.sleep(0.5)
        pool.makeInactive(name)

if __name__ == '__main__':
    pool = ThreadPool()
    s = threading.Semaphore(3)
    for i in range(10):
        t = threading.Thread(target=f, name='thread_'+str(i), args=(s, pool))
        t.start()
```

  
Output:

```
(thread_0 ) Waiting to join the pool
(thread_0 ) Running: ['thread_0']
(thread_1 ) Waiting to join the pool
(thread_1 ) Running: ['thread_0', 'thread_1']
(thread_2 ) Waiting to join the pool
(thread_2 ) Running: ['thread_0', 'thread_1', 'thread_2']
(thread_3 ) Waiting to join the pool
(thread_4 ) Waiting to join the pool
(thread_5 ) Waiting to join the pool
(thread_6 ) Waiting to join the pool
(thread_7 ) Waiting to join the pool
(thread_8 ) Waiting to join the pool
(thread_0 ) Running: ['thread_1', 'thread_2']
(thread_3 ) Running: ['thread_1', 'thread_2', 'thread_3']
(thread_1 ) Running: ['thread_2', 'thread_3']
(thread_4 ) Running: ['thread_2', 'thread_3', 'thread_4']
(thread_2 ) Running: ['thread_3', 'thread_4']
(thread_5 ) Running: ['thread_3', 'thread_4', 'thread_5']
(thread_3 ) Running: ['thread_4', 'thread_5']
(thread_6 ) Running: ['thread_4', 'thread_5', 'thread_6']
(thread_4 ) Running: ['thread_5', 'thread_6']
(thread_7 ) Running: ['thread_5', 'thread_6', 'thread_7']
(thread_5 ) Running: ['thread_6', 'thread_7']
(thread_8 ) Running: ['thread_6', 'thread_7', 'thread_8']
(thread_6 ) Running: ['thread_7', 'thread_8']
(thread_7 ) Running: ['thread_8']
(thread_8 ) Running: []
```

In the code, the `ThreadPool` class tracks which threads are able to run at a given moment. A real resource pool would allocate a connection or some other value to the newly active thread, and reclaim the value when the thread is done. Here it is used just to hold the names of the active threads to show that only 10 are running concurrently.



--------------------------------------------------------

# Thread specific data - threading.local()

Thread-local data is data whose values are thread specific. To manage thread-local data, just create an instance of local (or a subclass) and store attributes on it:

```python
mydata = threading.local()
mydata.x = 1
```

The instance's values will be different for separate threads.
- from https://docs.python.org/3/library/threading.html

While some resources need to be locked so multiple threads can use them, others need to be protected so that they are hidden from the views of threads that do not "own" them. The local() function creates an object capable of hiding values from view in separate threads.

```python
import threading
import logging
import random

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-0s) %(message)s',)

def show(d):
    try:
        val = d.val
    except AttributeError:
        logging.debug('No value yet')
    else:
        logging.debug('value=%s', val)

def f(d):
    show(d)
    d.val = random.randint(1, 100)
    show(d)

if __name__ == '__main__':
    d = threading.local()
    show(d)
    d.val = 999
    show(d)

    for i in range(2):
        t = threading.Thread(target=f, args=(d,))
        t.start()
```

Output:

```
(MainThread) No value yet
(MainThread) value=999
(Thread-1) No value yet
(Thread-1) value=51
(Thread-2) No value yet
(Thread-2) value=19
```

Note that local_data.value is not set for any thread until it is set in that thread.



### Subclassing threading.local

To initialize the settings so all threads start with the same value, we need to use a subclass and set the attributes in `__init__()`.

```python
import threading
import logging
import random

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',)

def show(d):
    try:
        val = d.val
    except AttributeError:
        logging.debug('No value yet')
    else:
        logging.debug('value=%s', val)

def f(d):
    show(d)
    d.value = random.randint(1, 100)
    show(d)

class MyLocal(threading.local):
    def __init__(self, v):
        logging.debug('Initializing %r', self)
        self.val = v

if __name__ == '__main__':
    d = MyLocal(999)
    show(d)

    for i in range(2):
        t = threading.Thread(target=f, args=(d,))
        t.start()
```

Output:

```
(MainThread) Initializing <__main__.MyLocal object at 0x7fc928e37b48>
(MainThread) value=999
(Thread-1  ) Initializing <__main__.MyLocal object at 0x7fc928e37b48>
(Thread-1  ) value=999
(Thread-1  ) value=999
(Thread-2  ) Initializing <__main__.MyLocal object at 0x7fc928e37b48>
(Thread-2  ) value=999
(Thread-2  ) value=999
```


--------------------------------------------------------

<sub>Source: http://www.bogotobogo.com/python/Multithread/<sub>