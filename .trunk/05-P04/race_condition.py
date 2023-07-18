import concurrent.futures


counter = 0
counter2 = 7
counter3 = 11


def increment_counter(fake_value):
    global counter
    global counter2
    global counter3
    for _ in range(100):
        counter2 -= 1
        counter3 += 1
        counter = counter2 + counter3


if __name__ == "__main__":
    fake_data = [x for x in range(5000)]
    counter = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=5000) as executor:
        executor.map(increment_counter, fake_data)

    print(counter)
