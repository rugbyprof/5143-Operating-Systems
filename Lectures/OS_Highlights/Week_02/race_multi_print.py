from multiprocessing import Process, Value
import os


def increment(counter):
    print(f"Process ID: {os.getpid()} Counter {counter.value} starting")
    for _ in range(100000):
        counter.value += 1  # Not atomic across processes!
    print(f"Process ID: {os.getpid()} Counter {counter.value} ending")


if __name__ == "__main__":
    from ctypes import c_int

    counter = Value(c_int, 0)
    procs = [Process(target=increment, args=(counter,)) for _ in range(5)]

    for p in procs:
        p.start()
    for p in procs:
        p.join()

    print("Expected:", 5 * 100000)
    print("Actual:", counter.value)
