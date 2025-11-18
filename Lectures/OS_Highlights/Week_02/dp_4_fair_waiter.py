#!/usr/bin/env python3
import threading
import time
import os, sys
import random

N = 5
names = ["Aristotle", "Kant", "Spinoza", "Marx", "Russell"]
forks = [threading.Lock() for _ in range(N)]
states = ["thinking"] * N
lock = threading.Lock()


current_philosopher = 0


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def display():
    global states
    global current_philosopher
    clear()
    print("🍝 Dining Philosophers Simulation (MSU OpSys Edition)")
    print("=" * 60)
    for i in range(N):
        state = states[i]
        color = {
            "thinking": "\033[94m",  # blue
            "hungry": "\033[93m",  # yellow
            "eating": "\033[92m",  # green
        }.get(state, "\033[0m")
        print(f"{color}{names[i]:>3}: {state:<10}\033[0m {current_philosopher}")
    print("=" * 60)
    print("Ctrl+C to stop.")
    time.sleep(0.2)


lock = threading.Lock()


def philosopher(i):
    global current_philosopher
    left, right = forks[i], forks[(i + 1) % N]
    name = names[i]

    while True:
        states[i] = "thinking"
        display()
        time.sleep(random.uniform(0.5, 1.5))
        states[i] = "hungry"
        display()
        time.sleep(random.uniform(0.5, 1.5))
        # with lock:
        #     my_turn = current_philosopher
        #     current_philosopher += 1

        while True:
            with lock:
                if current_philosopher == i:
                    break
            time.sleep(0.1)  # politely wait

        left.acquire()
        right.acquire()
        states[i] = "eating"
        display()
        time.sleep(random.uniform(1, 2))
        right.release()
        left.release()

        states[i] = "thinking"
        display()
        time.sleep(random.uniform(0.5, 1.5))

        with lock:
            current_philosopher = (current_philosopher + 1) % N


if __name__ == "__main__":

    threads = [
        threading.Thread(target=philosopher, args=(i,), daemon=True) for i in range(N)
    ]
    for t in threads:
        t.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSimulation ended by user.")
