from multiprocessing import Process, Value


def increment(counter):
    for _ in range(10000):
        counter.value += 1  # Not atomic across processes!


if __name__ == "__main__":
    from ctypes import c_int

    counter = Value(c_int, 0)
    procs = [Process(target=increment, args=(counter,)) for _ in range(5)]

    for p in procs:
        p.start()
    for p in procs:
        p.join()

    print("Expected:", 5 * 10000)
    print("Actual:", counter.value)
