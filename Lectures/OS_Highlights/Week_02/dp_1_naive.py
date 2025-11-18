#!/usr/bin/env python3
import threading
import time
import os
import random


N = 5
forks = [threading.Lock() for _ in range(N)]
names = ["Aristotle", "Kant", "Spinoza", "Marx", "Russell"]
states = ["thinking"] * N


# def think(name):
#     print(f"{name} is thinking...")
#     time.sleep(random.uniform(0.5, 1.5))


# def eat(name):
#     print(f"🍝 {name} is eating!")
#     time.sleep(random.uniform(0.5, 1.5))


# N = 5
# names = [f"P{i}" for i in range(N)]
# forks = [threading.Lock() for _ in range(N)]
# states = ["thinking"] * N
# lock = threading.Lock()


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def display():
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
        print(f"{color}{names[i]:>3}: {state:<10}\033[0m")
    print("=" * 60)
    print("Ctrl+C to stop.")
    time.sleep(0.2)


def philosopher(i):
    left = forks[i]
    right = forks[(i + 1) % N]

    while True:
        states[i] = "hungry"
        display()
        time.sleep(random.uniform(0.5, 1.5))
        left.acquire()
        # print(f"{i} Acquired left fork")
        right.acquire()
        # print(f"{i} Acquired right fork")
        states[i] = "eating"
        display()
        time.sleep(random.uniform(1, 2))
        left.release()
        right.release()
        states[i] = "thinking"
        display()
        time.sleep(random.uniform(0.5, 1.5))


threads = [
    threading.Thread(target=philosopher, args=(i,), daemon=True) for i in range(N)
]

for t in threads:
    t.start()
    t.join(0.01)


try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nSimulation ended by user.")
