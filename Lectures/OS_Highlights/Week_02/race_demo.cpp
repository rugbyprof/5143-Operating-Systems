// race_demo.cpp
#include <iostream>
#include <thread>
#include <vector>

long counter = 0;

void increment() {
    for (int i = 0; i < 100000; ++i) {
        // Not atomic: read -> modify -> write
        long temp = counter;
        temp += 1;
        counter = temp;
    }
}

int main() {
    std::vector<std::thread> threads;

    for (int i = 0; i < 5; ++i)
        threads.emplace_back(increment);

    for (auto& t : threads)
        t.join();

    std::cout << "Expected: " << 5 * 100000 << "\n";
    std::cout << "Actual:   " << counter << "\n";

    return 0;
}