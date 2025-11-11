# race_demo.py
import threading, time, random

counter = 0


def increment():
    global counter
    for _ in range(10000):
        # Not atomic: read, increment, write
        time.sleep(random.random() * 0.0001)
        temp = counter
        temp += 1
        counter = temp


threads = [threading.Thread(target=increment) for _ in range(5)]

for t in threads:
    t.start()
for t in threads:
    t.join()

print("Expected:", 5 * 1000)
print("Actual:", counter)
