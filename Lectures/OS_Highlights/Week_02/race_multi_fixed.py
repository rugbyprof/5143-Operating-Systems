# race_demo_multiprocessing_lock.py
from multiprocessing import Process, Value, Lock
from ctypes import c_int
import os


def increment(counter, lock):
    print(f"Process ID: {os.getpid()} Counter {counter.value} starting")
    for _ in range(100000):
        with lock:  # acquire + release automatically
            counter.value += 1
    print(f"Process ID: {os.getpid()} Counter {counter.value} ending")


if __name__ == "__main__":
    counter = Value(c_int, 0)
    lock = Lock()
    processes = [Process(target=increment, args=(counter, lock)) for _ in range(5)]

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    print("Expected:", 5 * 100000)
    print("Actual:", counter.value)
