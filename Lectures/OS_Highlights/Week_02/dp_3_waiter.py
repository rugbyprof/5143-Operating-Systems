waiter = threading.Semaphore(N - 1)


def philosopher(i):
    left = forks[i]
    right = forks[(i + 1) % N]
    name = names[i]

    while True:
        think(name)
        waiter.acquire()
        left.acquire()
        right.acquire()
        eat(name)
        right.release()
        left.release()
        waiter.release()
