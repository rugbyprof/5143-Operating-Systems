lock = threading.Lock()
next_turn = 0


def philosopher(i):
    global next_turn
    left, right = forks[i], forks[(i + 1) % N]
    name = names[i]

    while True:
        think(name)
        with lock:
            my_turn = next_turn
            next_turn += 1

        while True:
            with lock:
                if my_turn == 0:
                    break
            time.sleep(0.1)  # politely wait

        left.acquire()
        right.acquire()
        eat(name)
        right.release()
        left.release()

        with lock:
            next_turn = (next_turn + 1) % N
