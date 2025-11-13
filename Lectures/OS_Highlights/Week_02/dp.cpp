#include <atomic>
#include <chrono>
#include <condition_variable>
#include <iostream>
#include <mutex>
#include <queue>
#include <thread>
#include <vector>

using namespace std;

static const int N = 5;
static const int RUNTIME_MS = 3000;

// Visual display characters
// T = Thinking, H = Hungry, E = Eating
enum State { THINKING, HUNGRY, EATING };

// Shared display lock so output isn't garbled
mutex print_mtx;

void display_states(const vector<State>& st) {
  lock_guard<mutex> lock(print_mtx);
  for (int i = 0; i < N; i++) {
    char c = (st[i] == THINKING) ? 'T' : (st[i] == HUNGRY) ? 'H' : 'E';
    cout << c << " ";
  }
  cout << "\n";
}

// Sleep helper for realism
void msleep(int ms) { this_thread::sleep_for(chrono::milliseconds(ms)); }

void run_naive() {
  cout << "\n=== NAIVE VERSION (deadlock likely) ===\n";

  vector<mutex> forks(N);
  vector<State> state(N, THINKING);
  atomic<bool> running = true;

  auto philosopher = [&](int id) {
    int left = id;
    int right = (id + 1) % N;

    while (running) {
      state[id] = THINKING;
      display_states(state);
      msleep(100);

      // Naively pick left then right
      state[id] = HUNGRY;
      display_states(state);

      forks[left].lock();
      forks[right].lock();

      state[id] = EATING;
      display_states(state);
      msleep(100);

      forks[right].unlock();
      forks[left].unlock();
    }
  };

  vector<thread> threads;
  for (int i = 0; i < N; i++) threads.emplace_back(philosopher, i);

  msleep(RUNTIME_MS);
  running = false;
  for (auto& t : threads) t.join();
}

void run_weird() {
  cout << "\n=== WEIRD VERSION (asymmetric forks) ===\n";

  vector<mutex> forks(N);
  vector<State> state(N, THINKING);
  atomic<bool> running = true;

  auto philosopher = [&](int id) {
    int left = id;
    int right = (id + 1) % N;

    while (running) {
      state[id] = THINKING;
      display_states(state);
      msleep(100);

      state[id] = HUNGRY;
      display_states(state);

      if (id % 2 == 0) {
        forks[right].lock();
        forks[left].lock();
      } else {
        forks[left].lock();
        forks[right].lock();
      }

      state[id] = EATING;
      display_states(state);
      msleep(100);

      forks[left].unlock();
      forks[right].unlock();
    }
  };

  vector<thread> threads;
  for (int i = 0; i < N; i++) threads.emplace_back(philosopher, i);

  msleep(RUNTIME_MS);
  running = false;
  for (auto& t : threads) t.join();
}

void run_waiter() {
  cout << "\n=== WAITER VERSION (deadlock-free) ===\n";

  vector<mutex> forks(N);
  mutex waiter;  // Only N-1 philosophers allowed to try
  vector<State> state(N, THINKING);
  atomic<bool> running = true;

  auto philosopher = [&](int id) {
    int left = id;
    int right = (id + 1) % N;

    while (running) {
      state[id] = THINKING;
      display_states(state);
      msleep(100);

      state[id] = HUNGRY;
      display_states(state);

      // Waiter prevents circular wait
      lock_guard<mutex> lk(waiter);

      forks[left].lock();
      forks[right].lock();

      state[id] = EATING;
      display_states(state);
      msleep(100);

      forks[right].unlock();
      forks[left].unlock();
    }
  };

  vector<thread> threads;
  for (int i = 0; i < N; i++) threads.emplace_back(philosopher, i);

  msleep(RUNTIME_MS);
  running = false;
  for (auto& t : threads) t.join();
}

void run_fair_waiter() {
  cout << "\n=== FAIR WAITER VERSION (no starvation) ===\n";

  vector<mutex> forks(N);
  mutex waiter_mtx;
  condition_variable waiter_cv;
  queue<int> queue_order;  // FIFO queue
  vector<State> state(N, THINKING);
  atomic<bool> running = true;

  auto philosopher = [&](int id) {
    int left = id;
    int right = (id + 1) % N;

    while (running) {
      state[id] = THINKING;
      display_states(state);
      msleep(100);

      state[id] = HUNGRY;
      display_states(state);

      // Enqueue request
      {
        lock_guard<mutex> lock(waiter_mtx);
        queue_order.push(id);
      }

      // Wait until it's your turn
      unique_lock<mutex> lk(waiter_mtx);
      waiter_cv.wait(lk, [&] { return queue_order.front() == id; });

      // Now safely eat
      forks[left].lock();
      forks[right].lock();
      state[id] = EATING;
      display_states(state);
      lk.unlock();

      msleep(100);

      forks[right].unlock();
      forks[left].unlock();

      // Remove yourself from queue and notify next
      lk.lock();
      queue_order.pop();
      lk.unlock();
      waiter_cv.notify_all();
    }
  };

  vector<thread> threads;
  for (int i = 0; i < N; i++) threads.emplace_back(philosopher, i);

  msleep(RUNTIME_MS);
  running = false;
  {
    lock_guard<mutex> lock(waiter_mtx);
    while (!queue_order.empty()) queue_order.pop();
  }
  waiter_cv.notify_all();
  for (auto& t : threads) t.join();
}

void run_monitor() {
  cout << "\n=== MONITOR VERSION (classic textbook solution) ===\n";

  vector<State> state(N, THINKING);
  vector<mutex> mtx(N);
  mutex monitor_mtx;
  condition_variable cvs[N];
  atomic<bool> running = true;

  auto left = [&](int i) { return (i + N - 1) % N; };
  auto right = [&](int i) { return (i + 1) % N; };

  auto test = [&](int i) {
    if (state[i] == HUNGRY && state[left(i)] != EATING &&
        state[right(i)] != EATING) {
      state[i] = EATING;
      cvs[i].notify_one();
    }
  };

  auto philosopher = [&](int id) {
    while (running) {
      {
        lock_guard<mutex> lock(monitor_mtx);
        state[id] = THINKING;
        display_states(state);
      }
      msleep(100);

      {
        lock_guard<mutex> lock(monitor_mtx);
        state[id] = HUNGRY;
        display_states(state);
        test(id);
      }

      // Wait until allowed to eat
      {
        unique_lock<mutex> ul(monitor_mtx);
        cvs[id].wait(ul, [&] { return state[id] == EATING; });
      }

      msleep(100);  // Eat

      // Done eating
      {
        lock_guard<mutex> lock(monitor_mtx);
        state[id] = THINKING;
        test(left(id));
        test(right(id));
      }
    }
  };

  vector<thread> threads;
  for (int i = 0; i < N; i++) threads.emplace_back(philosopher, i);

  msleep(RUNTIME_MS);
  running = false;
  for (auto& t : threads) t.join();
}

int main() {
  cout << "Choose version:\n";
  cout << "1. naive\n";
  cout << "2. weird\n";
  cout << "3. waiter\n";
  cout << "4. fair_waiter\n";
  cout << "5. monitor\n";
  cout << "Selection: ";

  int choice;
  cin >> choice;

  switch (choice) {
    case 1:
      run_naive();
      break;
    case 2:
      run_weird();
      break;
    case 3:
      run_waiter();
      break;
    case 4:
      run_fair_waiter();
      break;
    case 5:
      run_monitor();
      break;
    default:
      cout << "Unknown choice\n";
  }

  return 0;
}