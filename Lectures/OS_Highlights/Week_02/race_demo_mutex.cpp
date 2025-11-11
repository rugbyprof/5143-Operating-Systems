// race_demo_mutex.cpp
#include <iostream>
#include <mutex>
#include <thread>
#include <vector>

long counter = 0;
std::mutex mtx;

void increment() {
  for (int i = 0; i < 100000; ++i) {
    std::lock_guard<std::mutex> lock(mtx);
    long temp = counter;
    temp += 1;
    counter = temp;
  }
}

int main() {
  std::vector<std::thread> threads;

  for (int i = 0; i < 5; ++i) threads.emplace_back(increment);

  for (auto& t : threads) t.join();

  std::cout << "Expected: " << 5 * 100000 << "\n";
  std::cout << "Actual:   " << counter << "\n";

  return 0;
}