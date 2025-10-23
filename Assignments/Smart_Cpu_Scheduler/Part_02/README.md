# 🧩 Operating Systems – Project Part 02

### Visualizing the Scheduler (Model + View + Controller)

---

## 📘 Overview

In **Part 01**, you extended the scheduler to include **arrival times** and a **time quantum** for Round Robin scheduling.  
You now have a functioning logical simulator that moves jobs through the CPU, I/O, and ready/wait queues based on time and state.

In **Part 02**, we will **separate** the scheduler logic from the user interface and create a **visualization layer** using `pygame`.  
This organization will make your simulator modular, testable, and ready to support future scheduling algorithms (FCFS, SJF, RR, Hybrid).

---

## 🧠 Design Goal – Separation of Concerns

You will divide your project into three main components:

| File                | Role                  | Knows About                                                |
| ------------------- | --------------------- | ---------------------------------------------------------- |
| **`scheduler.py`**  | Core simulation logic | Jobs, queues, bursts, quantum, arrival times               |
| **`visualizer.py`** | Pygame display layer  | Reads scheduler state, draws queues and jobs               |
| **`main.py`**       | Glue / controller     | Calls `scheduler.step()` and `visualizer.draw()` each tick |

This structure follows the **Model–View–Controller (MVC)** pattern:

> <sup>[Example Here](../Part_02/Visualization/003_mvc/)</sup>

```
+----------------+
|  main.py       |  → drives clock and loop
+----------------+
        |
        v
+----------------+     → pure logic (Model)
|  scheduler.py  |
+----------------+
        |
        v
+----------------+     → pure display (View)
|  visualizer.py |
+----------------+
```

---

## 🧩 Assignment Tasks

### 1️⃣ Refactor your existing scheduler

- Keep **all scheduling logic** in `scheduler.py`.
- Remove any print or timing code related to display.
- Add a method `snapshot()` that returns a dictionary of current state:

  ```python
  def snapshot(self):
      return {
          "clock": self.clock,
          "ready": [job.id for job in self.ready],
          "wait": [job.id for job in self.wait],
          "cpu": [job.id for job in self.cpu],
          "io": [job.id for job in self.io],
      }
  ```

This lightweight snapshot will be used by the visualizer.

---

### 2️⃣ Create a visualizer using Pygame

In `visualizer.py`:

- Draw rectangles for each queue (`Ready`, `Wait`, `CPU`, `IO`).
- Display job IDs (e.g., `P1`, `P2`, …) inside the queues.
- Update the display each tick by reading the scheduler’s snapshot.
- Keep it **read-only** — the visualizer should never modify the scheduler.

**Stretch Goal:**  
Different colors for full queues or running jobs.  
(Optional) Animate jobs sliding between queues.

---

### 3️⃣ Write a main controller

In `main.py`:

- Instantiate your `Scheduler` and `Visualizer`.
- Run a loop that:
  1. Calls `scheduler.step()`
  2. Calls `visualizer.update_from_scheduler()`
  3. Calls `visualizer.draw()`
- Add a small delay (`time.sleep(0.25)` or `pygame.time.wait(250)`) to control speed.

Example:

```python
while scheduler.has_jobs():
    scheduler.step()
    visualizer.update_from_scheduler()
    visualizer.draw()
```

---

## 🧩 Expected Output

- A **Pygame window** showing four queues stacked vertically.
- Job IDs appear in queues as the scheduler runs.
- CPU/IO queues enforce `max_size` limits visually.
- Simulation continues until all queues are empty.

---

## 🧠 Discussion Questions

Include short written answers (in a Markdown file or as comments):

1. Why is it valuable to separate the scheduler logic from the visualization layer?
2. How could this design be extended to run two schedulers at once (for comparison)?
3. What information should the visualizer _not_ have access to, and why?

---

## 📦 Deliverables

| File            | Description                                              |
| --------------- | -------------------------------------------------------- |
| `scheduler.py`  | Pure simulation logic with `step()` and `snapshot()`     |
| `visualizer.py` | Pygame renderer that draws queues and jobs               |
| `main.py`       | Control loop that ties everything together               |
| `README.md`     | Brief explanation of your architecture and how to run it |

---

## 🏁 Run Instructions

From your project folder:

```bash
python main.py
```

Press **ESC** or close the window to exit.

---

## 🔮 Coming Next – Part 03

In the next part, you’ll begin adding multiple scheduling algorithms  
(FCFS, SJF, Priority, Round Robin, and Hybrid)  
and visualize how each behaves under different arrival and burst patterns.

---

> “A scheduler without a visualization is like an OS without a user —  
> you know it works, but it’s way more fun to watch it think.”
